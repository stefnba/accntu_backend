from celery import shared_task, current_task, task

from selenium import webdriver 
from explicit import waiter, ID
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

import requests

import time

from accounts.models import Account
from .models import NewImport
from .providers.providers import provider_classes
from .parsing.parser import Parser
from .serializers import ImportSerializer

@task(bind=True)
def do_import(self, accounts, user):

    importable_transactions = []
    
    for account_id in list(accounts):
        
        account = Account.objects.get(id=account_id)
        key = account.provider.key

        # credentials
        # TODO encryption
        login = account.login
        login_sec = account.login_sec
        pin = account.pin


        Provider = provider_classes[key]

        self.update_state(
            state='PROGRESS',
            meta={
                'msg': 'Initiated import of {}'.format(account.title)
            }
        )
            
        # actual retrival of transactions through API or scrapping
        retriever = Provider(login, pin)


        # LOGIN



        # if login true, then send update -> login must return true/false

        # if 2factor, then call that method







        # TODO LOGIN
        self.update_state(
            state='PROGRESS',
            meta={
                'msg': 'Successfully logged in'
            }
        )

        time.sleep(0.5)


        # TODO transactions retrieved
        transactions_raw = retriever.return_transactions()

        self.update_state(
            state='PROGRESS',
            meta={
                'msg': '{} transactions retrieved'.format(len(transactions_raw))
            }
        )

        # parse raw transactions into importable transactions
        parser = Parser(
            data=transactions_raw,
            account=account_id,
            parser_map=account.provider.parser_map,
            provider=key
        )
        account_transactions = parser.return_parsed()


        # append retrieved transactions for given account
        importable_transactions.extend(account_transactions)

    # TODO import transactions
    serializer = ImportSerializer(
        data=importable_transactions,
        many=True, 
        context={'user': user}
    )

    if serializer.is_valid():
        
        # save new import
        new_import = NewImport.objects.create(
            user_id=user,
        )

        # save transactions
        saved = serializer.save(
            user_id=user,
            importing=new_import
        )

        saved = [t for t in saved if t is not False]
        res = {
            'transactions': 'to come',
            'nmbr': len(saved)
        }

        self.update_state(
            state='PROGRESS',
            meta={
                'msg': '{} transactions imported'.format(len(saved))
            }
        )

        time.sleep(0.5)

        return res

    print('not valid')
    print(serializer.errors)

    return serializer.errors














