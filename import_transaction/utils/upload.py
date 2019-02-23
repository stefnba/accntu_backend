from accounts.models import Account
from main.models import Transaction

import csv
import hashlib
import json

from io import StringIO



class ReadFromFile(object):
    
    ERORRS = {
        'FILE_SIZE': {
            'error': 'FILE_SIZE',
            'code': '001',
            'message': 'The file is too large'
        },
        'FILE_TYPE': {
            'error': 'FILE_TYPE',
            'code': '002',
            'message': 'The file must be of type .csv'
        }
    }
    
    
    def __init__(self, file=None, account=None):
        
        self.account = account
        self.errors = []
        self.transactions = {
            'import': [],
            'duplicate': [],
            'last': None
        }


        if file is not None and account is not None:
            # start process
            if self.check_file(file):
                reader = self.read_csv(file)
                self.map_csv_content(reader)
    
    
    def check_file(self, file):
        
        max_size = 10 # in MB
        allowed_endings = '.csv'
        allowed_content_type = 'text/csv'

        name = file.name
        content_type = file.content_type
        size = file.size

        # check for errors
        if size > max_size * 1000000:
            return self.throw_error('FILE_SIZE')

        if not name.endswith(allowed_endings) or not content_type == allowed_content_type:
            return self.throw_error('FILE_TYPE')
        
        # if no error
        return True

    def is_valid(self):
        print(self.errors)
        has_errors = len(self.errors) > 0

        if has_errors:
            return False

        return True


    def get_data(self):
        " return data based on mapping and extraction of csv "
        
        data = self.transactions 
        del data['last'] # delete last transaction
        return data

    def read_csv(self, csv_file):
        " Read content of csv "
        
        csv_file.seek(0)
        content = StringIO(csv_file.read().decode('utf-8', errors='ignore'))
        
        return csv.DictReader(content, delimiter=';')
        

    def throw_error(self, err):
        try:
            error = self.ERORRS[err]
            self.errors.append(error)
        except:
            print('no error code found')
        
        return False

    def get_error(self):
            return self.errors[0]

    " ======================================================= "

    def map_csv_content(self, file):
        " initiate mapping of csv content to transaction arrays "

        csv_file_content = file # csv rows of file
        account_mapping_dict = self.get_mapping_dict() # get mapping info from model field of that account
       
        # iterate over every row in csv, populate_transaction_from_csv_row does the acutal mapping of columns to fields
        for transaction_row_in_csv in csv_file_content: 
            transaction = self.populate_transaction_from_csv_row(transaction_row_in_csv, account_mapping_dict)
            set_array = 'import' # default: append all info from one row to import list

            if not transaction['is_unique']:
                set_array = 'duplicate'
            
            self.transactions[set_array].append(transaction)
            self.transactions['last'] = transaction
        

    def get_all_columns_for_field(self, transaction_row_in_csv, columns_to_field):
        " consolidate multiple columns in csv to one field "

        field_value = '' # empty to needed if value from multiple csv columns
                
        for column in list(columns_to_field):
            column_name_csv = column['column']
            column_regex = column['regex']
            field_value_before_cleaning = transaction_row_in_csv[column_name_csv]

            field_value_to_append = self.clean_field_value(
                field_value_before_cleaning, 
                column_regex
                )
            field_value += field_value_to_append
        
        return field_value


    def populate_transaction_from_csv_row(self, transaction_row_in_csv, account_mapping_dict):
        " based on row in csv, extract all data for transaction instance "

        keys_mapping_dict = list(account_mapping_dict.keys())
        transaction_row_container = {} # dict container for one row in csv
        
        # one field equals one field in model Transaction (e.g. date, title, amount, etc.)
        # iterate over every column in one csv row
        for field in keys_mapping_dict: 
            # several columns to one field, inlcude one csv row with all data and json data for given field
            field_value = self.get_all_columns_for_field(transaction_row_in_csv, account_mapping_dict[field])
            
            # populate all info for one field to transaction container    
            transaction_row_container[field] = field_value
        
        # hash part for duplicate check of given transaction
        hash_value = self.hash_transaction(transaction_row_container)
        transaction_row_container['hash_duplicate'] = hash_value # append hash to container
        transaction_row_container['is_unique'] = self.is_unique(hash_value)

        return transaction_row_container


    def get_mapping_dict(self):
        " return mapping dict for given account from database "
        
        qs = Account.objects.get(id=self.account)
        return qs.mapping


    def clean_field_value(self, field_value, regex):
        " extract correct field value, apply regex, etc. "
        
        return field_value


    def hash_transaction(self, current_transaction):
        " hash transaction with previous one to prevent duplicate imports "
        
        # confiq which fields included in hash
        keys_to_hash = ['date', 'title', 'spending_amount', 'spending_currency']
        additional_info_to_hash = [self.account, ]
        
        # get previous transaction       
        previous_transaction = self.transactions['last']
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