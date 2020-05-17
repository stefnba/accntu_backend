import threading
from celery import shared_task, current_task, task
from datetime import datetime

from .models import NewImport, NewImportOneAccount
from .providers.scrapping.utils import wait_for_tan
from .process.retriever import Retriever, retrieve_account_transactions

from .process.process_utils import pusher_trigger

from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from users.models import Settings



@task(bind=True)
def initiate_import(
        self,
        accounts=[],
        user=None, 
        upload=None
    ):
    """

    """

    task_id = self.request.id
    nmbr_imported_transactions = 0

    # pusher_trigger(
    #     task_id,
    #     'IMPORT_PROCESS',
    #     { 
    #         'msg': 'Import process has started ...',
    #         'progress_push': 10,
    #     }
    # )

    accounts = Account.objects.select_related(
        'user',
        'provider',
        'provider__import_details'
    ).filter(pk__in=accounts)
    
    # save new import object, will be completed later once process is complete
    new_import = NewImport.objects.create(
        user_id=user,
    )

    for account in accounts:

        retriever = Retriever(
            account.user,
            account,
            task_id,
            new_import
        )
        
        if upload:
            retriever.upload(upload)

        new_transactions = retriever.retrieve_transactions()

        # save transaction to db (# of saved trx is returned)
        nmbr_imported_transactions += retriever.save(new_transactions)

    # update new_import object if import successful
    if nmbr_imported_transactions > 0:

        new_import.import_success = True
        new_import.nmbr_transactions = nmbr_imported_transactions
        new_import.save()

        # pusher_trigger(
        #     task_id,
        #     'IMPORT_SUCCESS',
        #     { 
        #         'msg': 'Import has been successful',
        #         'progressbar': 100,
        #         'count': nmbr_imported_transactions
        #     }
        # )

        return {
            'transactions': 'to come',
            'nmbr': nmbr_imported_transactions
        }

    print('not updated')

    return {

    }



@task(bind=True)
def initiate_import_old(self, accounts=[], user=None, upload=None):
    """
    Celery task triggered by view ImportViaAPI in views.py, handles threading of parallel import with calling
    function retrieve_account_transactions as defined in process/retriever.py
    After that, initiates serializer ImportSerializer in serializers.py
    """

    importable_transactions = []
    task_id = self.request.id.__str__()


    # save new import object, will be completed later once process is complete
    new_import = NewImport.objects.create(
        user_id=user,
    )

    # get additional user information, like user currency
    user_currency = Settings.objects.filter(user_id=user).first().user_currency


    # trigger start msg
    pusher_trigger(
        task_id,
        'IMPORT_PROCESS',
        { 
            'msg': 'Import process has started ...',
            'progress_push': 10,
        }
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
                importable_transactions,
                upload,
            )
        )

        threads.append(thread)
        thread.start()


    # wait until all retrieving has finished
    for thread in threads: 
        thread.join()

    pusher_trigger(
        task_id,
        'IMPORT_PROCESS',
        { 
            'msg': 'Preparing importing of {} transactions'.format(len(importable_transactions)),
            'progress_push': 10,
        }
    )
    

    """
    Start actual importing process, e.g. serialization
    """

    serializer = ImportSerializer(
        data=importable_transactions,
        many=True, 
        context={'user': user}
    )


    if serializer.is_valid():

        # save transactions to db and add user_id
        saved = serializer.save(
            user_id=user,
        )

        # get number of saved transactions, False means that duplicate already existed in db
        imported_trx = [trx for trx in saved if trx is not False]
        nmbr_imported_trx = len(imported_trx)


        # update entire import object
        new_import.import_success = True
        new_import.nmbr_transactions = nmbr_imported_trx
        new_import.save(update_fields=['import_success', 'nmbr_transactions'])

        """
        Update ech account import instances as well as account info like last_import and first_import_success
        """

        for import_account in accounts:

            """

            """
            nmbr_imported_trx_account = len([trx for trx in imported_trx if trx.account_id is import_account])

            new_import_one_account = NewImportOneAccount.objects.filter(
                account_id=import_account,
                new_import=new_import
            )

            if not new_import_one_account:
                continue
            
            new_import_one_account.update(
                nmbr_transactions=nmbr_imported_trx_account,
                import_success=True,
            )

            if nmbr_imported_trx_account is 0:
                print('No transactions have been imported for this account!')
                continue

            """
            Update account
            """

            acc = Account.objects.filter(pk=import_account)

            if not acc:
                continue

            acc.update(
                last_import=datetime.now(),
                first_import_success=True,
            )



        # trigger success messages
        pusher_trigger(
            task_id,
            'IMPORT_SUCCESS',
            { 
                'msg': 'Import has been successful',
                'progressbar': 100,
                'count': nmbr_imported_trx
            }
        )


        return {
            'transactions': 'to come',
            'nmbr': nmbr_imported_trx
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














