
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from explicit import waiter, ID
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

from accounts.models import Account
from ..models import NewImport, NewImportOneAccount, ImportDetails, Upload

# from ..providers.providers import provider_classes


from .parsing.parser import Parser
from .process_utils import pusher_trigger
from .api.api_providers import api_providers




def retrieve_account_transactions(
        user,
        user_currency,
        account_id,
        task_id,
        new_import,
        importable_transactions,
        upload,
    ):
    """
    Initiate import of one account
    """

    # retrieve account info
    account = Account.objects.filter(id=account_id).first()

    # continue with next account, return zero transactions
    if not account:
        print('no account found')
        return []

    
    # create db object in model NewImportOneAccount for import of this account
    new_import_one_account = NewImportOneAccount.objects.create(
        user_id=user,
        new_import = new_import,
        account=account
    )


    # get parser_dict from db
    parser_qs = ImportDetails.objects.filter(provider__account__id=account_id).first()
    if not parser_qs:
        return []
    parser_dict = model_to_dict(parser_qs)


    # if upload id is provided then type upload
    if upload:
        print('upload')
        
        u = Upload.objects.filter(id=upload).first()

        # no upload found in db
        if not u:
            return []

        if parser_dict['file_type'] == 'csv':
            transactions_file = str(u.upload_file.read().decode(encoding=parser_dict['file_encoding']))
        else:
            transactions_file = u.upload_file

    # if None then type import
    else:

        # credentials
        # TODO encryption
        login = account.login
        login_sec = account.login_sec
        pin = account.pin


        """
        Web scraping access
        """
        if account.provider.access_type == 'scr':
            print('scrapping')
            pass


        """
        API access
        """
        if account.provider.access_type == 'api':
            print('api')

            print(account.provider.key)

            APIClass = api_providers[account.provider.key]

            api = APIClass(
                account_id,
                login,
                pin
            )

            transactions_file = api.get_transactions()
            




    """
    Parse raw transactions into importable transactions
    """

    # parse raw transactions as returned by api or web scrapper
    parser = Parser(
        parser_dict=parser_dict,
        file=transactions_file,
        account={
            'account_id': account_id,
            'account_name': 'TEST_NAME' # TODO
        },
        importing_id=new_import_one_account.id,
        user_currency=user_currency
    )

    # returns dict
    transactions_parsed = parser.parse()

    # trigger parsed msg
    pusher_trigger(
        task_id,
        'IMPORT_PROCESS',
        {
            'msg': '{}: transactions parsed'.format(account.title),
            'progress': 10,
        }
    )

    """
    Update account import
    """
        
    new_import_one_account.import_success = True
    new_import_one_account.nmbr_transactions = len(transactions_parsed)
    new_import_one_account.save(update_fields=['import_success', 'nmbr_transactions', 'raw_csv'])
    
    # save raw and parsed csv file to db (file is used to distinguish both files)
    new_import_one_account.raw_csv.save('raw', parser.save_csv('raw'))
    new_import_one_account.parsed_csv.save('parsed', parser.save_csv('parsed'))


    # final step: append transactions of that account to list importable_transactions
    importable_transactions.extend(transactions_parsed)
    








"""
def OLD():    
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


    

)


"""