from datetime import datetime

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
        

    def iteratve_csv_rows(self):
        """ 
            Iterate over every row in csv and for each row, call map_csv_columns_of_row.
            In addition, add also additional info to each transaction like key, account, etc. 
        """
        
        account = self.account
        
        for index, csv_row in enumerate(self.csv_content, start=1):
            transaction  = self.map_csv_columns_of_row(csv_row, account.mapping)

            # return if error
            if not transaction:
                return False

            # add additional information to each transaction
            transaction['key'] = index
            transaction['account'] = int(account.id)
            transaction['spending_account_rate'] = round(float(transaction['account_amount'] / transaction['spending_amount']), 4)

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
                if map_info_of_field is None:
                    print('ERROR: Field', field, 'is missing')
                    return self.throw_error('FIELD_MISSING')
                
                # extract content of column
                row_container[field] = self.extract_field(field, map_info_of_field, csv_row)

                print(row_container)
        return row_container
        

    def extract_field(self, field, map_info_of_field, csv_row):
        """

        """

        column_options_for_field = DB_FIELDS[field].get('options', None)
        field_type = DB_FIELDS[field].get('type', None)

        # return if None
        if column_options_for_field is None and field_type is None:
            return None

        column_options = {column_option: map_info_of_field.get(column_option, None) 
            for column_option in column_options_for_field}
        
        return getattr(self, 'get_content_' + field_type)(
            field, 
            column_options,
            csv_row
        )

    
    def get_content_amount_field(self, field, column_options, csv_row):        
        """

        """

        amount = csv_row.get(column_options['column'], None)

        # use secondary column if value of column is ''
        if amount is not None and amount is '':
            amount = csv_row.get(column_options['column_secondary'], None)

        # use debit and credit column if column not provided
        if amount is None:
            debit = csv_row.get(column_options['column_debit'], None)
            credit = csv_row.get(column_options['column_credit'], None)

            # TODO here
            # TODO set cache for credit/debit
            # self.meta_cache.append({'status': 'debit'})
            print('noooooone')

        # return None if still no value for amount 
        if amount is None:
            return None

        # otherwise clean amount
        amount_cleaned = self.clean_amount_field1(
            amount, 
            column_options['negative_for_debit'],
            column_options['thousand_sep'],
            column_options['decimal_sep']
        )

        return amount_cleaned
            
            

    def clean_amount_field1(self, amount, negative_for_debit, thousand_sep, decimal_sep):
        """
            set right status (debit or credit), clean negative sign, ...
            thousand sep and decimal sep.
        """
        cleaned_amount = amount

        # in case debit/credit same column and distinguished by minus sign
        if negative_for_debit:
            # debit
            if '-' in amount:
                cleaned_amount = cleaned_amount.replace('-', '')
                self.meta_cache.append({'status': 'debit'})

            # credit
            if '-' not in amount:
                self.meta_cache.append({'status': 'credit'})
        
        # remove thousand sep
        if thousand_sep:
            cleaned_amount = cleaned_amount.replace(thousand_sep, '')

        # replace decimal sep
        if decimal_sep == ',':
            cleaned_amount = cleaned_amount.replace(',', '.')


        return float(cleaned_amount)


    def extract_amount_field(self, field, account_mapping, csv_row):
        """
            Get amount valued from relevant fields. 
            Also initiate cleaning of columns.
        """


        map_info_of_field = account_mapping.get(field, None)
        column_name = map_info_of_field.get('column', None)


        # column_secondary = map_info_of_field.get('column_secondary', None)
        # column_debit = map_info_of_field.get('column_debit', None)
        # column_credit = map_info_of_field.get('column_credit', None)
        # default = map_info_of_field.get('default', None)
        # regex = map_info_of_field.get('regex', None)
        # has_negative = map_info_of_field.get('has_negative', None)
        # decimal_sep = map_info_of_field.get('decimal_sep', None)
        # thousand_sep = map_info_of_field.get('thousand_sep', None)

        # if account has mapping like "column": "Amount (EUR)"
        if isinstance(column_name, str):
            amount = csv_row.get(column_name, None)

            # return cleaned amount if cell not empty
            if (amount and amount is not ''):
                return self.clean_amount_field(amount, map_info_of_field)

            # return cleaned amount if secondary column was used
            if amount is '':
                secondary_column_name = map_info_of_field.get('secondary_column', None)
                amount = csv_row.get(secondary_column_name, None)

                if (amount and amount is not ''):
                    return self.clean_amount_field(amount, map_info_of_field)


        # if account has mapping like "column": { "debit_colum": "xxx", "credit_column": "yyy" }
        if isinstance(column_name, dict):
            # TODO
            amount = 2

            # return cleaned amount only if cell not empty
            if (amount and amount is not ''):
                return self.clean_amount_field(amount, map_info_of_field, False)

        return None


    def clean_amount_field(self, amount, map_info_of_field, credit_or_debit=None):
        """
            set right status (debit or credit), clean negative sign, thousand sep and decimal sep
        """

        cleaned_amount = amount

        negative_for_debit = map_info_of_field.get('negative_for_debit', None)
        thousand_sep = map_info_of_field.get('thousand_sep', None)
        decimal_sep =  map_info_of_field.get('decimal_sep', None)

        # in case debit/credit same column and distinguished by minus sign
        if negative_for_debit and not credit_or_debit:
            if '-' in amount:
                cleaned_amount = cleaned_amount.replace('-', '')

                # set cache to status negative, i.e. debit
                self.meta_cache.append({'status': 'debit'})

            if '-' not in amount:
                # set cache to status positive, i.e. credit
                self.meta_cache.append({'status': 'credit'})

        # set debit transaction
        if credit_or_debit == 'debit':
            # set cache to status negative, i.e. debit
            self.meta_cache.append({'status': 'debit'})

        # set credit transaction
        if credit_or_debit == 'credit':
            # set cache to status positive, i.e. credit
            self.meta_cache.append({'status': 'credit'})

        # remove thousand sep
        if thousand_sep:
            cleaned_amount = cleaned_amount.replace(thousand_sep, '')


        # replace decimal sep
        if decimal_sep == ',':
            cleaned_amount = cleaned_amount.replace(',', '.')


        return float(cleaned_amount)


    def extract_date_field(self, csv_row, account_mapping, field_name):
        """
            
        """

        # set weekday for date
        days = [
            'Mon', 'Tue', 'Wed',
            'Thu', 'Fri', 'Sat',
            'Sun',
        ]

        map_info_of_field = account_mapping.get(field_name, None)
        column_name = map_info_of_field.get('column', None)
        date_format = map_info_of_field.get('format', '%d.%m.%y')

        date = csv_row.get(column_name, None)

        # get day
        date = datetime.strptime(date, date_format).date()

        # weekday
        day = date.weekday()
        self.meta_cache.append({'day': days[day]})

        return date.__str__()



    def throw_error(self, err):
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

