import csv, hashlib, os, re
from datetime import datetime
# from decimal import Decimal

import json
import pandas as pd
import numpy as np

from io import StringIO

from .parser_utils import remove_umlaut, FXRate 




class Parser(object):

    def __init__(
        self,
        parser_dict,
        file,
        account,
        importing_id,
        user_currency
    ):
        
        self.parser_dict = parser_dict
        self.file = file
        self.account = account
        self.importing_id = importing_id
        self.user_currency = user_currency


        self.df = pd.DataFrame()
        self.import_df = pd.DataFrame()


    def extract_currency(self, item):
        """

        """

        currency = re.search(r'([$€£]{1}|[a-zA-Z]{3})', str(item))
        
        if currency:
            return currency.group()
        
        return item


    def convert_currency(self, item):
        
        if item in '$€£':
            
            curr_map = {
                    '$': 'USD',
                    '€': 'EUR',
                    '£': 'GBP'
                }
                
            return curr_map[item]
            
        return item


    def clean_status(self, item):

        status_col_map = self.parser_dict['status_col_map']
        
        if item == status_col_map['credit']:
            return 'credit'
        
        if item == status_col_map['debit']:
            return 'debit'
        
        return None


    def clean_amount(self, item, col):    
    
        item = str(item)

        # clean amount of any currency characters 
        if (col is 'spending_amount' and self.parser_dict['spending_amount_col_has_currency']) or (col is 'account_amount' and self.parser_dict['account_amount_col_has_currency']):
            currency = self.extract_currency(item)        
            item = item.replace(currency, '')
        
        
        # remove thousend sep
        if (col is 'account_amount' and self.parser_dict['account_amount_thousand_sep'] == '.') or (col is 'spending_amount' and self.parser_dict['spending_amount_thousand_sep'] == '.'):
            item = item.replace('.', '')
            
        if (col is 'account_amount' and self.parser_dict['account_amount_thousand_sep'] == '\'') or (col is 'spending_amount' and self.parser_dict['spending_amount_thousand_sep'] == '\''):
            item = item.replace('\'', '')
        
        # convert decimal sep
        item = item.replace(',', '.')
        
        if self.parser_dict['account_amount_col_has_status']:
            item = item.replace('-', '')
        
        return round(float(item), 2)


    # Clean date
    def clean_title(self, item):
    
        item = remove_umlaut(item)
        return item



    def read_file(self):

        # Create DFs (StringIO necessary to read from variable/memory)
        if self.parser_dict['file_type'] == 'csv':
            self.import_df = pd.read_csv(
                StringIO(self.file),
                sep = self.parser_dict['csv_sep'],
                skiprows = self.parser_dict['skiprows'],
                encoding = self.parser_dict['file_encoding'],
                error_bad_lines = False
            )
        
        elif self.parser_dict['file_type'] == 'xls':
            self.import_df = pd.read_excel(
                self.file,
                skiprows = self.parser_dict['skiprows']    
            )
        
        else:
            # TODO Raise error
            pass

        # drop some colums (e.g. abgerechnet oder nicht), necessary i.a. for key generation
        self.import_df = self.import_df.drop(columns=list(self.parser_dict['cols_to_drop']))

    
    def _initiate_parsing_process(self):
        """
        Do actual parsing process
        """

        # Clean date
        self.df['date'] = pd.to_datetime(self.import_df[self.parser_dict['date_col']], format=self.parser_dict['date_format']).dt.date


        # Clean account currency
        if self.parser_dict['account_currency_col'] is None:
            if self.parser_dict['account_amount_col_has_currency']:
                self.df['account_currency'] = self.import_df[self.parser_dict['account_amount_col']].apply(self.extract_currency).apply(self.convert_currency)
                
            else:
                self.df['account_currency'] = self.parser_dict['account_currency_default']
        
        else:
            self.df['account_currency'] = self.import_df[self.parser_dict['account_currency_col']]

        # Clean spending currency
        
        # Regular column
        if self.parser_dict['spending_currency_col'] is not None:
            self.df['spending_currency'] = self.import_df[self.parser_dict['spending_currency_col']]

        if self.parser_dict['spending_currency_col'] is None and self.parser_dict['spending_amount_col_has_currency']:
            self.df['spending_currency'] = self.import_df[self.parser_dict['spending_amount_col']].apply(self.extract_currency).apply(self.convert_currency)


        # where spending currency is NaN, fallback to account currency
        if self.parser_dict['spending_currency_fallback_to_account_currency']:
            self.df['spending_currency'] = np.where(self.df['spending_currency'] == 'nan', self.parser_dict['account_currency_default'], self.df['spending_currency'])

        
        # User currency
        self.df['user_currency'] = self.user_currency


        # Clean title
        self.df['title'] = self.import_df[self.parser_dict['title_col']].apply(self.clean_title)


        # Clean country
        if self.parser_dict['country_col'] is not None:
            self.df['country'] = self.import_df[self.parser_dict['country_col']]
        else:
            self.df['country'] = None


        # Clean status
        if self.parser_dict['status_col'] is None:
            if self.parser_dict['account_amount_col_has_status']:
                self.df['status'] = self.import_df[self.parser_dict['account_amount_col']].apply(lambda item: 'debit' if '-' in str(item) else 'credit')
        else:
            self.df['status'] = self.import_df[self.parser_dict['status_col']].apply(self.clean_status)


        # Fill NaN of spending amount col with 0
        self.import_df[self.parser_dict['spending_amount_col']] = self.import_df[self.parser_dict['spending_amount_col']].fillna(0)

        cleaned_spending_amount = self.import_df[self.parser_dict['spending_amount_col']].apply(self.clean_amount, args=('spending_amount',)).apply(pd.to_numeric)
        cleaned_account_amount = self.import_df[self.parser_dict['account_amount_col']].apply(self.clean_amount, args=('account_amount',)).apply(pd.to_numeric)

        # Clean spending amount
        if self.parser_dict['spending_amount_fallback_to_account_amount']:
            self.df['spending_amount'] = np.where(self.import_df[self.parser_dict['spending_amount_col']] == 0, cleaned_account_amount, cleaned_spending_amount)
        else:
            self.df['spending_amount'] = cleaned_spending_amount


        # Clean account amount
        self.df['account_amount'] = cleaned_account_amount


        # Spending to account rate
        self.df['spending_account_rate'] = round(self.df['account_amount'] / self.df['spending_amount'], 4)


        # Account to user rate
        self.df['account_user_rate'] = self.df.apply(lambda row: FXRate.get_rate(date=row.date, transaction_currency=row.account_currency, counter_currency=self.user_currency), axis=1).astype(np.float64)
        
        
        # User amount
        self.df['user_amount'] = round(self.df['account_amount'] * self.df['account_user_rate'], 2)

        # Importing
        self.df['importing'] = self.importing_id


        # Account
        self.df['account'] = self.account['account_id']


        # Create key with occs and assign to transaction
        self.df['all_cols'] = self.import_df.astype(str).values.sum(axis=1)
        counts = self.df['all_cols'].value_counts()
        count_col = self.df['all_cols'].map(counts)
        self.df['all_cols'] = self.df['all_cols'] + str(count_col)
        self.df['hash_duplicate'] = self.df['all_cols'].apply(lambda item: hashlib.md5((item).encode('utf-8')).hexdigest())
        
        self.df = self.df.drop(columns=['all_cols'])


    def parse(self):
        """
        Initiate parsing process
        """
        
        # read file or data in memory
        self.read_file()

        # to parsing
        self._initiate_parsing_process()

        # save parsed file
        self.to_csv(self.df, 'parsed')

        # return parsed transactions for given account (returns dict)
        return self.df.to_dict('records')

    
    def to_csv(self, df, mode):

        loc = 'importing/imports/' + self.account['account_name'] + '/'
        now = datetime.now().strftime("%Y%m%d-%I%M")
        filename = str(now + '_' + mode + '.csv')

        # make dir
        os.makedirs(loc, exist_ok=True)

        # save df to csv
        df.to_csv(loc + filename)





