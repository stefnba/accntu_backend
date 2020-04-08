import threading

from celery import shared_task, current_task, task

from .models import NewImport, NewImportOneAccount
from .providers.scrapping.utils import wait_for_tan
from .serializers import ImportSerializer
from .process.start import retrieve_account_transactions


from .process.process_utils import pusher_trigger


@task(bind=True)
def do_import(self, accounts, user):
    """

    """

    importable_transactions = []
    task_id = self.request.id.__str__()


    # save new import
    new_import = NewImport.objects.create(
        user_id=user,
    )


    # trigger start msg
    pusher_trigger(
        task_id,
        'import_process',
        'Import process has started ...'
    )


    # initiate threading for parallel importing of multiple accounts
    threads = []
    
    for account_id in list(accounts):
        
        # start one thread for each account to be imported/updated
        thread = threading.Thread(
            target=retrieve_account_transactions,
            args=(
                user, 
                account_id, 
                task_id, new_import, 
                importable_transactions
            )
        )

        threads.append(thread)
        thread.start()


    # wait until all retrieving has finished
    for thread in threads: 
        thread.join()

    """
    Start actual importing process, e.g. serialization
    """
    
    pusher_trigger(
        task_id,
        'import_process',
        'Preparing importing of {} transactions'.format(len(importable_transactions))
    )

    print(importable_transactions)


    serializer = ImportSerializer(
        data=importable_transactions,
        many=True, 
        context={'user': user}
    )


    if serializer.is_valid():

        # save transactions
        saved = serializer.save(
            user_id=user,
            # importing=new_import_one_account
        )

        saved = [t for t in saved if t is not False]
        nmbr_transactions = len(saved)


        # update entire import
        new_import.import_success = True
        new_import.nmbr_transactions = nmbr_transactions
        new_import.save(update_fields=['import_success', 'nmbr_transactions'])

        pusher_trigger(
            task_id,
            'import_process',
            'Import successful'
        )

        return {
            'transactions': 'to come',
            'nmbr': nmbr_transactions
        }


    pusher_trigger(
        task_id,
        'import_error',
        'There was a problem. Transactions couldn\'t be imported!'
    )

    print('not valid')
    print(serializer.errors)

    return serializer.errors














