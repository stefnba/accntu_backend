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


















"------------------------------------ OLD ------------------------------------"

class ReadFromFile(object):
    
    
    
    
    def __init__(self, file=None, account=None):
        
        self.account = account
        self.account_confiq = {}
        self.errors = []
        self.transactions = []
        self.transaction_cache = []


        if file is not None and account is not None:
            # start process
            if self.check_file(file):
                reader = self.read_csv(file)
                self.map_csv_content(reader)
    
    

    

    " ======================================================= "

    def map_csv_content(self, file):
        " initiate mapping of csv content to transaction arrays "

        csv_file_content = file # csv rows of file
        account_mapping_dict = self.get_mapping_dict() # get mapping info from model field of that account
       
        # iterate over every row in csv, populate_transaction_from_csv_row does the acutal mapping of columns to fields
        for index, transaction_row_in_csv in enumerate(csv_file_content, start=1): 
            transaction = self.populate_transaction_from_csv_row(transaction_row_in_csv, account_mapping_dict)

            

            # set account
            transaction['account'] = self.account
            transaction['title_original'] = 'ddddddd'
            
            self.transactions.append(transaction)        


    def get_all_columns_for_field(self, transaction_row_in_csv, columns_to_field, field):
        " consolidate multiple columns in csv to one field "

        field_value = '' # empty to needed if value from multiple csv columns

        for column in list(columns_to_field):
            column_name_csv = column.get('column', None)
            column_regex = column.get('regex', None)
            
            separator = column.get('separator', '')

            # which key is used to get column value, e.g. column, default, secondary_column, ...
            key_used = 'column'

            # check if account json contains 'column' key, if know attempt for default value
            if column_name_csv is not None:
                field_value_before_cleaning = dict(transaction_row_in_csv).get(column_name_csv, None)

                # use secondary column if column is empty in csv
                secondary_column = column.get('secondary_column', None)
                if field_value_before_cleaning == '' and secondary_column is not None:
                    field_value_before_cleaning = dict(transaction_row_in_csv).get(secondary_column, None)
                    key_used = 'secondary_column'

                if field_value_before_cleaning is None:
                    print('key not found: ', column)
            
            # default column value
            column_default = column.get('default', None)
            if (column_name_csv is None and column_default is not None) or (field_value_before_cleaning == '' and column_default is not None):
                field_value_before_cleaning = 'EUR'  
                key_used = 'default'


            print(field_value_before_cleaning)           


            # clean field value
            field_value_to_append = self.clean_field_value(
                field_value_before_cleaning, # value
                column, # column including name in csv and regex
                field, # column name in model
                key_used,
            )
            
            # check if variable is string, then append
            if isinstance(field_value_to_append, str):
                field_value += separator + field_value_to_append

            else:
                field_value = field_value_to_append
        
        return field_value


    def populate_transaction_from_csv_row(self, transaction_row_in_csv, account_mapping_dict):
        " based on row in csv, extract all data for transaction instance "

        keys_mapping_dict = list(account_mapping_dict.keys())
        transaction_row_container = {} # dict container for one row in csv
        
        # one field equals one field in model Transaction (e.g. date, title, amount, etc.)
        # iterate over every column in one csv row
        for field in keys_mapping_dict: 
            # several columns to one field, inlcude one csv row with all data and json data for given field
            field_value = self.get_all_columns_for_field(transaction_row_in_csv, account_mapping_dict[field], field)
            
            # populate all info for one field to transaction container    
            transaction_row_container[field] = field_value
        
        # hash part for duplicate check of given transaction
        hash_value = self.hash_transaction(transaction_row_container)
        transaction_row_container['hash_duplicate'] = hash_value # append hash to container
        transaction_row_container['is_unique'] = self.is_unique(hash_value)

        # set transaction attributes from cache & clean cache
        for item in self.transaction_cache:
            for key, value in item.items():
                transaction_row_container[key] = value
        self.transaction_cache = []
        
        return transaction_row_container



    def get_mapping_dict(self):
        " return mapping dict for given account from database "
        
        qs = Account.objects.get(id=self.account)

        # set account conqiq (necessary for cleaning column fields)
        self.account_confiq = {
            'decimal_sep': qs.decimal_sep,
            'thousand_sep': qs.thousand_sep,
            'has_negativesign': qs.has_negativesign
        }

        # return only mapping
        return qs.mapping



    def clean_field_value(self, field_value, column, field, key_used):
        " extract correct field value, apply regex, etc. "
        
        fields_to_clean = [
            { 'field_name': 'spending_amount', 'type': 'amount_field' },
            { 'field_name': 'account_amount', 'type': 'amount_field' },
            { 'field_name': 'spending_account_rate', 'type': 'amount_field' },
            { 'field_name': 'date', 'type': 'date_field' },
            { 'field_name': 'title', 'type': 'string_field' },
        ]

        cleaned_value = field_value # in case no cleaning happens

        # check if field requires cleaning (if in fields_to_clean)
        if any(field_to_clean.get('field_name', None) == field for field_to_clean in fields_to_clean):
            # TODO CLEANING
            cleaning_action = [d['type'] for d in fields_to_clean if d['field_name'] == field][0]
            
            cleaned_value = getattr(self, 'clean_'+ cleaning_action)(field_value, column, key_used) 

        # clean regex
        # if column['regex'] is 'NULL':
        #     print(123)
        #     # TODO

        return cleaned_value



    def clean_date_field(self, field_value, column, key_used):
        

        # set weekday for date
        days = [
            'Mon', 'Tue', 'Wed',
            'Thu', 'Fri', 'Sat',
            'Sun',
        ]

        # get day
        date_format = column.get('format', '%d.%m.%y')
        date = datetime.strptime(field_value, date_format).date()

        # weekday
        day = date.weekday()
        self.transaction_cache.append({'day': days[day]})

        return date.__str__()



    def clean_string_field(self, field_value, column, key_used):
        return field_value



    def hash_transaction(self, current_transaction):
        " hash transaction with previous one to prevent duplicate imports "
        
        # confiq which fields included in hash
        keys_to_hash = ['date', 'title', 'spending_amount', 'spending_currency']
        additional_info_to_hash = [self.account, ]
        
        # get previous transaction       
        previous_transaction = self.transactions[-1] if len(self.transactions) > 0 else None
        previous_transaction_for_hash = []

        # prepare previous transaction for hash
        if previous_transaction is not None:
            previous_transaction_for_hash = [previous_transaction[i] for i in keys_to_hash] + additional_info_to_hash

        # prepare current transaction for hash
        current_transaction_for_hash = [current_transaction[i] for i in keys_to_hash] + additional_info_to_hash

        # hash both transactions
        return self.hash_list(current_transaction_for_hash + previous_transaction_for_hash)
        


    def hash_list(self, list):
        " does actual hasing "
        
        return hashlib.md5(json.dumps(list, sort_keys=True).encode('utf-8')).hexdigest()



    def is_unique(self, hash):
        " check if transaction exists in database already based on hash "
        
        return Transaction.objects.filter(hash_duplicate=hash).count() == 0