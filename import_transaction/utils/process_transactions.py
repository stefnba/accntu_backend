import hashlib
import json
import re

from datetime import datetime

from transactions.models import Transaction

from .import_errors import ERORRS
from .import_fields import DB_FIELDS


""" 
    Process csv file and return all transactions to parent class
     
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ProcessTransactions(object):    
    def __init__(self):
        self.errors = []
        self.meta_cache = []
        self.transaction_list = []
        self.prev_csv_row = None
        

    def iteratve_csv_rows(self):
        """ 
            Iterate over every row in csv and for each row, call map_csv_columns_of_row.
            In addition, add also additional info to each transaction like key, account, etc. 
        """
        
        account = self.account
        csv_content = self.csv_content

        
        for index, csv_row in enumerate(csv_content, start=1):
            transaction  = self.map_csv_columns_of_row(csv_row, account.mapping)

            # return if error
            if not transaction:
                return False

            # add additional information to each transaction
            transaction['key'] = index
            transaction['account'] = int(account.id)
            transaction['spending_account_rate'] = round(float(transaction['account_amount'] / transaction['spending_amount']), 4)

            # hash part for duplicate check of given transaction
            hash_value = self.hash_row(csv_row, self.prev_csv_row)
            is_unique = self.is_unique(hash_value)

            transaction['hash_duplicate'] = hash_value # append hash to container
            transaction['is_unique'] = is_unique
            transaction['is_import'] = is_unique # if user deselected trx

            # necessary for hashing of next csvh row
            self.prev_csv_row = csv_row 
            
            # set transaction attributes from cache & clean cache
            for item in self.meta_cache:
                for key, value in item.items():
                    transaction[key] = value
            self.meta_cache = []
            
            self.transaction_list.append(transaction)

        return self.transaction_list  


    def map_csv_columns_of_row(self, csv_row, account_mapping):
        """
            Process all columns for one row in csv file.
            Extraction and cleaning of all fields (method extract_xxx and then clean_xxx).
        """

        row_container = {}

        # get fields required for transaction and iterate over them.
        # but first check if row is valid transaction, i.e. account_amount must not be empty. 
        fields = list(DB_FIELDS.keys())

        map_info_of_field = account_mapping.get('account_amount', None)
        account_amount = self.extract_field('account_amount', map_info_of_field, csv_row)

        # extract fields only if account_account not zero or empty
        if account_amount:
            
            row_container['account_amount'] = account_amount
            fields.remove('account_amount') # remove account_amount as already extracted

            for field in fields:
                
                map_info_of_field = account_mapping.get(field, None)
                
                # error if required field is missing
                required = DB_FIELDS[field].get('mandatory', True)
                if map_info_of_field is None and required:
                    print('ERROR: Field', field, 'is missing')
                    return self.throw_error('FIELD_MISSING')
                
                # skip to next if field is missing but not required
                if map_info_of_field is None and not required:
                    continue

                # extract content of column
                row_container[field] = self.extract_field(field, map_info_of_field, csv_row)

        return row_container
        

    def extract_field(self, field, map_info_of_field, csv_row):
        """
            Gathers all column attributes, e.g. column, column_secondary, into [{ }]
            Then calls set_field_value()
        """

        column_options_for_field = DB_FIELDS[field].get('options', None)
        field_type = DB_FIELDS[field].get('type', None)
        map_info_multiple = DB_FIELDS[field].get('multiple', False)

        # return if options equals None
        if column_options_for_field is None and field_type is None:
            print('List not allowed for field')
            return None

        # return if map_info is list but no multiple allowed for field
        if isinstance(map_info_of_field, list) and not map_info_multiple:
            return None

        # populate dict with all column attributes
        # e.g. column, column_second, default, etc.        
        # depending on if list or just string
        if isinstance(map_info_of_field, list):
            field_attrs = [
                {
                    field_attr: map_item.get(field_attr, None)
                        for field_attr in column_options_for_field
                } for map_item in map_info_of_field
            ]
        
        else:
            field_attrs = [{
                field_attr: map_info_of_field.get(field_attr, None) 
                    for field_attr in column_options_for_field
            }]

        return self.set_field_value(csv_row, field, field_attrs, field_type)


    def set_field_value(self, csv_row, field, field_attrs, field_type):
        """

        """



        field_value = []
        attrs_is_list = len(field_attrs) > 1

        for index, field_attr in enumerate(field_attrs):

            # add additional parameters to field_attr
            field_attr['index'] = index
            field_attr['field_value'] = field_value
            
            value = csv_row.get(field_attr['column'], None)

            # extract regex
            regex = field_attr['regex']
            if regex:
                result = re.search(regex, value)
                # r'\s(\w{3})\s\d'
                if result:
                    value = result.group(1)

                    # necessary as Barclaycard has . in regex, other is , as decimal
                    if field_type == 'amount_field':
                        value = value.replace('.', field_attr['decimal_sep'])

                # if no value
                else:
                    value = None


            # use secondary column if value of column is ''
            if (value is not None and value is '') or value is None:
                value = csv_row.get(field_attr['column_secondary'], None)

            # use default if value of secondary column is also '' (or none)
            if value is None or value is '':
                value = field_attr['default']

            # clean value
            cleaned_value = getattr(self, 'clean_' + field_type)(
                value, 
                csv_row,
                field,
                field_attr
            )

            if isinstance(cleaned_value, list):
                # many text field returns list, thus extend
                field_value.extend(cleaned_value)
            else:
                # append value to field_value list
                field_value.append(cleaned_value)
                

        """
            Define finale value based on field_value
            Either convert list to string if only one value, 
            or join list items to string
        """

        if not attrs_is_list:
            final_value = field_value[0]
        else:
            final_value = ''.join(filter(None, field_value))

        # if value is None, then return None
        if final_value is None:
            return None

        # return final value
        return final_value

    
    def clean_amount_field(self, value, csv_row, field, field_attr):
        """

        """

        amount = value

        # use separate debit and credit column if column not provided
        if amount is None:
            debit = csv_row.get(field_attr['column_debit'], None)
            credit = csv_row.get(field_attr['column_credit'], None)

            # set debit
            if credit is '' and debit is not '':
                amount = debit

                if field == 'account_amount':
                    self.meta_cache.append({'status': 'debit'})

            if credit is not '' and debit is '':
                amount = credit

                if field == 'account_amount':
                    self.meta_cache.append({'status': 'credit'})

        # return None if still no value for amount 
        if amount is None:
            return None

        
        """
            set right status (debit or credit), clean negative sign, ...
            thousand sep and decimal sep.
        """

        cleaned_amount = amount
        negative_for_debit = field_attr['negative_for_debit']
        thousand_sep = field_attr['thousand_sep']
        decimal_sep = field_attr['decimal_sep']

        # in case debit/credit same column and distinguished by minus sign
        if negative_for_debit:
            # debit
            if '-' in amount:
                cleaned_amount = cleaned_amount.replace('-', '')
                if field == 'account_amount':
                    self.meta_cache.append({'status': 'debit'})

            # credit
            if '-' not in amount:
                if field == 'account_amount':
                    self.meta_cache.append({'status': 'credit'})
        
        # remove thousand sep
        if thousand_sep:
            cleaned_amount = cleaned_amount.replace(thousand_sep, '')

        # replace decimal sep
        if decimal_sep == ',':
            cleaned_amount = cleaned_amount.replace(',', '.')

        print(cleaned_amount)

        return float(cleaned_amount)


    
    def clean_date_field(self, value, csv_row, field, field_attr):
        """
            Sets date, weekday, weeknumber
        """

        # set weekday for date
        days = [
            'Mon', 'Tue', 'Wed',
            'Thu', 'Fri', 'Sat',
            'Sun',
        ]

        # content of csv
        date_csv = value
        # date_format = csv_row.get(field_attr['format'], '%d.%m.%y')
        date_format = field_attr.get('format', '%d.%m.%y')
        print(field_attr);
        print(field_attr['format']);
        
        # date
        date = datetime.strptime(date_csv, date_format).date()

        # weekday
        day = date.weekday()
        self.meta_cache.append({'day': days[day]})

        # week
        week = date.isocalendar()[1]
        self.meta_cache.append({'week': week})

        return date.__str__()


    def clean_text_field(self, value, csv_row, field, field_attr):



        # TODO ignore word, to upper, to lower etc.
        if field == 'title':
            value = self.clean_title(value, field_attr)
        
        """
            Integrate separator if not fir
        """
        value_list = field_attr['field_value']
        if len(value_list) > 0:
            if value_list[0] is not None and value is not None and field_attr['sep'] is not None:
                sep = ' ' + field_attr['sep'] + ' '
                return [sep, value]
            else:
                return value

        return value
    

    def clean_title(self, title, field_attr):

        stopwords = ['*', 'com', ',', 'ag']
        upperwords = ['AG', 'CHF', 'DEU', 'HK']
        lowerwords = ['www', 'im', 'of', 'or', 'from', 'in']

       

        stopwords_account = field_attr.get('stopwords', None)
        
        if stopwords_account is not None:
            stopwords_joint = stopwords + list(stopwords_account)
        else: 
            stopwords_joint = stopwords

        # print(stopwords_joint)


        if title is None:
            return None

        words = re.split(r'\.|\s+|\,', title)

        # print(words)
        
        # remove words and make first letter capitalized
        words[:] = [word.title() for word in words if word.lower() not in stopwords_joint]

        # print(words)
        
        # lowerwords 
        words[:] = [word.lower() if word.lower() in lowerwords else word for word in words]

        # upperwords
        words[:] = [word.upper() if word.upper() in upperwords else word for word in words]

        return ' '.join(words)




    def hash_row(self, csv_row, prev_csv_row):
        """ 
            Hash csv row
        """
        
        # convert csv row values to list
        hash_row = list(csv_row.values())

        # include prev rows if exists
        if prev_csv_row:
            hash_row = hash_row + list(prev_csv_row.values())

        return hashlib.md5(json.dumps(hash_row, sort_keys=True).encode('utf-8')).hexdigest()


    def is_unique(self, hash):
        """ 
            Check if transaction exists in database already based on hash
        """
        
        return Transaction.objects.filter(hash_duplicate=hash).count() == 0
            


    def throw_error(self, err):
        """
            Appends error to error list
        """

        try:
            error = ERORRS[err]
            self.errors.append(error)
        except:
            print('no error code found')
        
        # if error was report, always return False
        return False


    @classmethod
    def transactions(cls, csv_content, account):
        """
            Method called by parent class. Return all transactions to it ...
            by callend _transactions
        """
        trx = cls()
        trx.csv_content = csv_content
        trx.account = account

        # initiate extraction and return transactions
        return trx.iteratve_csv_rows()

