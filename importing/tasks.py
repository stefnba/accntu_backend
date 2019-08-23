from celery import shared_task, current_task, task
from django.core.exceptions import ObjectDoesNotExist

from decouple import config
from pusher import Pusher
from explicit import waiter, ID
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

import csv, requests, time, threading


from accounts.models import Account
from .models import NewImport, NewImportOneAccount
from .providers.providers import provider_classes
from .parsing.parser import Parser
from .providers.scrapping.utils import wait_for_tan
from .serializers import ImportSerializer


pusher_client = Pusher(
  app_id=config(u'PUSHER_APP_ID'),
  key=config(u'PUSHER_KEY'),
  secret=config(u'PUSHER_SECRET'),
  cluster=config(u'PUSHER_CLUSTER')
)

pusher_event_name = 'import_process'
pusher_error_event_name = 'import_error'


def import_error(task_id, msg):
    print(msg)
    
    pusher_client.trigger(task_id, pusher_error_event_name, {
        'message': msg
    })



def retrieve_account_transactions(user, account_id, task_id, new_import, importable_transactions):
    try: 
        account = Account.objects.get(id=account_id)
    except ObjectDoesNotExist: 
        
        import_error(task_id, "Account {} doesn't exist!".format(account_id))

        # continue with next account
        return []


    """ if account exists, execute below """
    new_import_one_account = NewImportOneAccount.objects.create(
        user_id=user,
        new_import = new_import,
        account=account
    )


    key = account.provider.key

    # credentials
    login = account.login
    login_sec = account.login_sec
    pin = account.pin

    # TODO encryption

    Provider = provider_classes[key]

    pusher_client.trigger(task_id, pusher_event_name, {
        'message': '{}: import initiated ...'.format(account.title)
    })
        
    # actual retrival of transactions through API or scrapping
    retriever = Provider()

    # account login
    login = retriever.login(login, pin, login_sec)

    # check and execute two factor
    if hasattr(retriever, 'login_two_factor'):

        url = retriever.login_two_factor(user, account_id)

        pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: waiting for Two-Factor Auth...'.format(account.title)
        })
        
        pusher_client.trigger(task_id, 'two_factor', {
            'two_factor': {
                'account': account_id,
                'task': task_id,
                'tan_id': url
            }
        })

        tan = wait_for_tan(user, account_id, task_id)

        if tan:
            pusher_client.trigger(task_id, pusher_event_name, {
                'message': '{}: TAN submitted...'.format(account.title)
            })
            
            retriever.login_two_factor_submit_tan(tan)
        
        else:
            login = False

            import_error(task_id, "{}: TAN submission failed!".format(account.title))
            
            # continue with next account
            return []


    if login:

        pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: login successful!'.format(account.title)
        })

    
    # if login not successful
    else:
        import_error(task_id, "{}: login not successful!".format(account.title))
        
        # continue with next account
        return []

    transactions_raw = retriever.get_raw_transactions(import_id=new_import_one_account.pk, csv_meta=account.provider.csv_meta)

    nmbr_transactions = len(transactions_raw)
    
    if nmbr_transactions > 0:
        pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: {} transactions retrieved'.format(account.title, len(transactions_raw))
        })

    else:
        import_error(task_id, "{}: no transactions retrieved!".format(account.title))

        # continue with next account
        return []


    # parse raw transactions into importable transactions
    parser = Parser(
        data=transactions_raw,
        account=account_id,
        parser_map=account.provider.parser_map,
        provider=key
    )
    account_transactions = parser.return_parsed()

    pusher_client.trigger(task_id, pusher_event_name, {
            'message': '{}: transactions parsed'.format(account.title)
        })

    # update account import
    # TODO has all transaction, should be only unique ones
    new_import_one_account.import_success = True
    new_import_one_account.nmbr_transactions = len(account_transactions)
    new_import_one_account.save(update_fields=['import_success', 'nmbr_transactions'])

    # add importing id for each transaction
    account_transactions = [dict(item, **{'importing': new_import_one_account.id }) for item in account_transactions]


    importable_transactions.extend(account_transactions)
    


@task(bind=True)
def do_import(self, accounts, user):

    importable_transactions = []
    task_id = self.request.id.__str__()

    # save new import
    new_import = NewImport.objects.create(
        user_id=user,
    )

    pusher_client.trigger(task_id, pusher_event_name, {
        'message': 'Import process has started ...'
    })


    threads = []
    
    for account_id in list(accounts):
        thread = threading.Thread(target=retrieve_account_transactions, args=(user, account_id, task_id, new_import, importable_transactions))
        threads.append(thread)
        thread.start()

    # wait until all retrieving has finished
    for thread in threads: 
        thread.join()

    """ Import transactions """

    pusher_client.trigger(task_id, pusher_event_name, {
        'message': 'Preparing importing of {} transactions'.format(len(importable_transactions))
    })

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


        pusher_client.trigger(task_id, pusher_event_name, {
            'message': 'Import successful'
        })

        return {
            'transactions': 'to come',
            'nmbr': nmbr_transactions
        }


    import_error(task_id, "There was a problem. Transactions couldn't be imported!")
    print('not valid')
    print(serializer.errors)

    return serializer.errors














