from .settings import IMPORT_FIELDS
# from providers.settings import PROVIDERS_META

from .cleaner import Cleaner

import re
import csv
from datetime import datetime
import os

class Parser(object):

    def __init__(self, data=[], account=None, parser_map={}, provider=None):

        self.data = data
        self.provider = provider
        self.account = account

        
        # trx caching
        self.transactions = []
        self.add_info = {}

        # parsing caching
        self.parser_map = parser_map
        self.list_item = None
        self.field = None
        
        


    def iterate_list_with_data(self):
        """ Iterate over every single item in list. First step """

        for list_item in self.data:

            # for caching
            self.list_item = list_item
            
            # parse one item (i.e. one transaction)
            transaction = self.parse_transaction_item()
            
            # append transaction to transaction cache
            self.transactions.append(transaction)

        return True
            

    def parse_transaction_item(self):
        """ For one item, assign column/cell content to each fieldname """

        one_transaction = {}
        fieldnames = list(IMPORT_FIELDS.keys())

        for fieldname in fieldnames:
            
            # for caching
            self.field = fieldname

            # parse cell value
            field_value = self.get_field_value()
            one_transaction[fieldname] = field_value

            # other add info
            other_add_info = {
                'account': self.account,
            }

            # merge with additional infos
            one_transaction = {** one_transaction, **self.add_info, **other_add_info}
        
        return one_transaction


    def get_field_value(self):
        """ Logic for converting cell value into field value by inititate cleaning, etc. 
            Cell value is the plain content of the csv, field value the cleaned content """

        # retrieve from cache
        field_map = self.parser_map.get(self.field, None)
    
        # get cell value
        cell_value = str(self.get_cell_value())

        # print(self.field, cell_value)

        # make cell value to field_value
        c =  Cleaner(cell_value, self.field, field_map)
        field_value = c.get_cleaned_value()
        add_info = c.get_add_info()

        # merge with additional infos, if any
        if len(add_info) > 0:
            self.add_info = {**self.add_info, **add_info}
       
        return field_value


    def get_cell_value(self):
        """ Logic for extracting cell value 
            Cell value is the plain content of the csv, field value the cleaned content """

        # retrieve from cache
        # field_map is mapping info of one field
        # list_item is one row/transaction/item in list of dictionaries
        field_map = self.parser_map.get(self.field, None)
        list_item = self.list_item

        if field_map is None:
            return None

        # assign columns to variables
        col_name = field_map.get('col', None)
        col_sec_name = field_map.get('col_sec', None)
        col_def_name = field_map.get('col_def', None)
        def_value = field_map.get('def', None)


        
        ### DEFAULT VALUE ###
        # if only default value is specified, e.g. Barclaycard for account currency
        if col_name is None and col_sec_name is None and col_def_name is None and def_value is not None:
            # print('default value returned', self.field)
            return def_value
        
        ### STANDARD COLUMN VALUE ###
        
        # get standard column value
        cell_value = list_item.get(col_name, None)

        # regex for standard column
        regex = field_map.get('reg', None)
        
        # if regex is None:
        #     return cell_value

        if regex:
            r = re.search(regex, cell_value)
            if r:
                cell_value = r.group(1)
                return cell_value

        # return standard column value if successfully retrieved
        elif cell_value is not None and cell_value is not '':
            # print('return standard column value if successfully retrieved')
            
            if self.field == 'account_amount' and '-' not in str(cell_value) and col_sec_name is not None:
                print('spending_column', cell_value)
                return str(cell_value + '-')
                
            return cell_value
        
        
        # print('cell v', self.field, cell_value)
        
        ### SECONDARY COLUMN VALUE
        
        # get secondary column value
        cell_value = list_item.get(col_sec_name, None)

        if cell_value is not None and cell_value is not '':
            



            return cell_value
        
        
        ### DEFAULT COLUMN VALUE

        # get default column value
        cell_value = list_item.get(col_def_name, None)

        if cell_value is not None and cell_value is not '':
            return cell_value


        ### DEFAULT VALUE

        return def_value


        # if cell_value is None or cell_value is '':
        #     cell_value = list_item.get(col_sec_name, None)

        # get cell value from default column
        # if cell_value is None or cell_value is '':
        #     cell_value = list_item.get(col_def_name, None)


        # return default VALUE if no default COLUMN is specified
        # if col_def_name is None:
        #     return def_value
        
        ### DEFAULT COLUMN VALUE
        # value of default column
        # return list_item[col_def_name]


    def to_csv(self, data, mode):

        loc = 'importing/imports/' + self.provider + '/'
        now = datetime.now().strftime("%Y%m%d-%I%M")
        filename = str(now + '_' + mode + '.csv')

        # make dir
        os.makedirs(loc, exist_ok=True)

        
        keys = list(IMPORT_FIELDS.keys()) + ['status', 'account']

        with open(loc + filename, 'w') as f:
            dict_writer = csv.DictWriter(f, keys, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(data)

            f.close()
            return True

        return False


    def return_parsed(self):
        
        # save raw transactions to csv
        # save_raw = self.to_csv(self.data, 'parsed')

        if self.iterate_list_with_data():
            # save parsed transactions to csv
            self.to_csv(self.transactions, 'parsed')

            return self.transactions
        
        

    