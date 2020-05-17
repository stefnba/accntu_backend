
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from explicit import waiter, ID
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

from django.core.files import File

from accounts.models import Account
from ..models import NewImport, NewImportOneAccount, ImportDetails, Upload
from ..serializers import ImportSerializer

# from ..providers.providers import provider_classes

from .parsing.parser import Parser
from .process_utils import pusher_trigger
from .api.api_providers import api_providers





class Retriever(object):

    def __init__(
            self,
            user,
            account,
            task_id,
            new_import
        ):
        """

        """
        self.user = user
        self.account = account
        self.parser_dict = model_to_dict(account.provider.import_details)
        self.transactions_file = None
        self.task_id = task_id

        # save new_import_one_account already to db
        self.new_import_one_account = self.save_import_process(new_import)


    def retrieve_transactions(self):
        """
        Entry point for retrieving transactions
        :return: parsed transactions via self._parse()
        """

        # if transactions already extracted via self.upload()
        if self.transactions_file:
            print('already upload')
            return self._parse()

        login = self.account.login
        login_sec = self.account.login_sec
        pin = self.account.pin
       
        if self.account.provider.access_type == 'api':
            self.transactions_file = self.retrieve_via_api(
                    login,
                    login_sec,
                    pin
                )


        if self.account.provider.access_type == 'scr':
            pass
            

        return self._parse()



    def retrieve_via_api(self, login, login_sec, pin):
        """
        Initiates api retrieval
        :param login: username of account
        :param login_sec: second login 
        :param pin: pin of account
        :return: list of transactions
        """

        print('Account requires API access for query of transactions')

        APIClass = api_providers[self.account.provider.key]

        api = APIClass(
            self.account.id,
            login,
            pin
        )

        return api.get_transactions(
            sub_accounts=list(self.account.sub_account.all()),
            first_import_success=self.account.first_import_success,
            last_import=self.account.last_import,
        )


    def upload(self, upload):
        """
        """
        
        print('Import via upload')
        
        upload_qs = Upload.objects.filter(id=upload).first()

        # no upload found in db
        if not upload_qs:
            return False

        file_type = self.parser_dict['file_type']
        encoding = self.parser_dict['file_encoding']

        if file_type  == 'csv':
            self.transactions_file = str(upload_qs.upload_file.read().decode(encoding=encoding))
        else:
            self.transactions_file = upload_qs.upload_file


    def save(self, transactions_to_import):
        """
        :param transactions_to_import: list of transactions 
        :return: # of imported transactions, if error or all trx already in db, then 0 is returned
        """

        serializer = ImportSerializer(data=transactions_to_import, many=True)

        if serializer.is_valid():

            print('ImportSerializer is valid')

            imported_transactions = serializer.save()
            nmbr_imported_transactions = len([trx for trx in imported_transactions if trx is not False])

            # update relevant db entries
            self.update_import_process(nmbr_imported_transactions)
            self.update_account_meta()

            return nmbr_imported_transactions


        print('ImportSerializer not valid')
        print(serializer.errors)
        return 0


    def update_account_meta(self):
        """
        Update info in Account model for fields like last_import, first_import_success
        """

        self.account.last_import = self.new_import_one_account.imported_at
        self.account.first_import_success = True
        
        self.account.save()



    def save_import_process(self, new_import):
        """
        Create db object in model NewImportOneAccount for import of this account
        """

        new_import_one_account = NewImportOneAccount.objects.create(
            user=self.user,
            new_import = new_import,
            account=self.account,
        )

        return new_import_one_account


    def update_import_process(self, nmbr_imported_transactions):
       
        self.new_import_one_account.raw_csv.save(
            'raw',
            self.csv_files['raw_csv'],
            save=False
        )

        self.new_import_one_account.parsed_csv.save(
            'parsed',
            self.csv_files['parsed_csv'],
            save=False
        )

        self.new_import_one_account.import_success = True
        self.new_import_one_account.nmbr_transactions = nmbr_imported_transactions
       

        self.new_import_one_account.save()


    def _parse(self):
        """
        :return: list of parsed transactions
        """

        parser = Parser(
            user=self.user,
            account=self.account,
            parser_dict=self.parser_dict,
            importing=self.new_import_one_account,
            file=self.transactions_file,
        )

        # # returns dict
        transactions_parsed = parser.parse()

        print(self.new_import_one_account)

        self.csv_files = {
            'raw_csv': parser.save_csv('raw'),
            'parsed_csv': parser.save_csv('parsed')
        }

        return transactions_parsed














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
    account = Account.objects.prefetch_related('sub_account').filter(id=account_id).first()

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
        print('Import via upload')
        
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
            print('Account requires scrapping for query of transactions')
            pass


        """
        API access
        """
        if account.provider.access_type == 'api':
            print('Account requires API access for query of transactions')

            APIClass = api_providers[account.provider.key]

            api = APIClass(
                account_id,
                login,
                pin
            )

            transactions_file = api.get_transactions(
                sub_accounts=list(account.sub_account.all()),
                first_import_success=account.first_import_success,
                last_import=account.last_import,
            )

            # exit if transactions_file was no success
            if not transactions_file:
                print('Exit since transactions_file was no success')
                return False

    print(transactions_file)

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
    new_import_one_account.raw_csv.save('raw', parser.save_csv('raw'))
    new_import_one_account.parsed_csv.save('parsed', parser.save_csv('parsed'))

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
    Update account import info
    """
        
    # new_import_one_account.import_success = True
    # new_import_one_account.nmbr_transactions = len(transactions_parsed)
    # new_import_one_account.save(update_fields=['import_success', 'nmbr_transactions', 'raw_csv'])
    
    # save raw and parsed csv file to db (file is used to distinguish both files)


    """
    FINAL STEP:
    Append transactions of that account to list importable_transactions
    """
    importable_transactions.extend(transactions_parsed)
