import hashlib
import json

from datetime import datetime
from decimal import Decimal

from accounts.models import Account
from transactions.models import Transaction
from .import_errors import ERORRS
from .read_csv import ReadCSV
from .process_transactions import ProcessTransactions




""" 
    Parent class that handles the entire extraction process and return ...
    list of all transaction back to view "
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ExtractTransactions(object):

    def __init__(self, csv_file=None, account=None):
        self.account = account
        self.errors = []
        self.transactions = []
        self.transaction_attribute_cache = []

        if csv_file is not None and account is not None:
            csv = ReadCSV(csv_file)
            if csv.is_valid():
                
                # get account dict
                accout_info = Account.objects.get(id=self.account)
                
                # get csv content
                csv_content = csv.get_content()
                
                # process csv content with account mapping info
                self.transactions = ProcessTransactions.transactions(csv_content, accout_info)
            
            else: 
                csv_errors = csv.get_errors()
                self.errors.append(csv_errors)
    


    def is_valid(self):
        " check if entire process has no errors "

        has_errors = len(self.errors) > 0

        if has_errors:
            return False

        return True



    def get_data(self):
        " return data to send to client "
        
        return self.transactions 

    

    def get_errors(self):
            return self.errors[0]



    def throw_error(self, err):
        try:
            error = ERORRS[err]
            self.errors.append(error)
        except:
            print('no error code found')
        
        # if error was report, always return False
        return False
