import threading
from celery import shared_task, current_task, task

from .models import NewImport, NewImportOneAccount
from .providers.scrapping.utils import wait_for_tan
from .serializers import ImportSerializer
from .process.start import retrieve_account_transactions

from .process.process_utils import pusher_trigger

from django.core.exceptions import ObjectDoesNotExist
from users.models import Settings


@task(bind=True)
def do_import(self, accounts, user):
    """
    Celery task triggered by view ImportViaAPI in views.py, handles threading of parallel import with calling
    function retrieve_account_transactions as defined in process/start.py
    After that, initiates serializer ImportSerializer in serializers.py
    """

    importable_transactions = []
    task_id = self.request.id.__str__()


    # save new import object, will be completed later once process is complete
    new_import = NewImport.objects.create(
        user_id=user,
    )

    # get additional user information, like user currency
    user_currency = Settings.objects.filter(user_id=1).first().user_currency


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
        # call function retrieve_account_transactions as defined in process/start.py
        thread = threading.Thread(
            target=retrieve_account_transactions,
            args=(
                user, 
                user_currency,
                account_id, 
                task_id,
                new_import, 
                importable_transactions
            )
        )

        threads.append(thread)
        thread.start()


    # wait until all retrieving has finished
    for thread in threads: 
        thread.join()

    pusher_trigger(
        task_id,
        'import_process',
        'Preparing importing of {} transactions'.format(len(importable_transactions))
    )


    print(importable_transactions)
    

    """
    Start actual importing process, e.g. serialization
    """

    serializer = ImportSerializer(
        data=importable_transactions,
        many=True, 
        context={'user': user}
    )


    if serializer.is_valid():

        # save transactions and add user_id
        saved = serializer.save(
            user_id=user,
        )

        # get number of saved transactions, False means that duplicate already existed in db
        saved = [t for t in saved if t is not False]
        nmbr_transactions = len(saved)


        # update entire import object
        new_import.import_success = True
        new_import.nmbr_transactions = nmbr_transactions
        new_import.save(update_fields=['import_success', 'nmbr_transactions'])


        # trigger success messages
        pusher_trigger(
            task_id,
            'import_process',
            'Import successful'
        )


        return {
            'transactions': 'to come',
            'nmbr': nmbr_transactions
        }


    """
    Serialization error
    """

    pusher_trigger(
        task_id,
        'import_error',
        'There was a problem. Transactions couldn\'t be imported!'
    )

    print('not valid')
    print(serializer.errors)

    return serializer.errors














