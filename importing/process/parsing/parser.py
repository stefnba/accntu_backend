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
        user,
        account,
        parser_dict,
        importing,
        file,
    ):
        
        self.parser_dict = parser_dict
        self.file = file
        self.account = account
        self.importing = importing
        self.user = user


        self.df = pd.DataFrame()
        self.import_df = pd.DataFrame()


    def extract_currency(self, item):
        """
        Get currency (e.g. EUR or €) from string
        """

        currency = re.search(r'([$€£]{1}|[a-zA-Z]{3})', str(item))
        
        if currency:
            return currency.group()
        
        return item


    def convert_currency(self, item):
        """
        Translate currency symbol into ISO code
        """
        
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

        if item == '':
            item = 0
        
        return round(float(item), 2)

    # Clean date
    def clean_title(self, item):

        item = str(item)

        if item == 'nan':
            return None

        # Remove douple spaces
        item = re.sub(' +', ' ', item)
    
        # Remove Umlaute
        item = remove_umlaut(item)
        
        return item


    def read_file(self):

        # Create DFs (StringIO necessary to read from variable/memory)

        file_encoding = self.parser_dict['file_encoding']
        if file_encoding is None:
            file_encoding = 'utf-8'

        sep = self.parser_dict['csv_sep']
        if sep is None:
            sep = ','

        if self.parser_dict['file_type'] == 'csv':

        
            self.import_df = pd.read_csv(
                StringIO(self.file),
                sep=sep,
                skiprows=self.parser_dict['skiprows'],
                encoding=file_encoding,
                error_bad_lines=False
            )
        
        elif self.parser_dict['file_type'] == 'xls':
            self.import_df = pd.read_excel(
                self.file,
                skiprows = self.parser_dict['skiprows']    
            )

        elif self.parser_dict['file_type'] == 'dict':
            self.import_df = pd.DataFrame(self.file)
        
        else:
            # TODO Raise error
            pass

        # drop some colums (e.g. abgerechnet oder nicht), necessary i.a. for key generation
        self.import_df = self.import_df.drop(columns=list(self.parser_dict['cols_to_drop']))


    def clean_date(self, item):
        """
        :param item: date to be parsed to date object
        :return: pandas date object
        """

        date_format = self.parser_dict['date_format']

        if date_format == 'timestamp_ms':
            return pd.to_datetime(item, unit='ms').date()

        else:
            return pd.to_datetime(item, format=date_format).date()

    
    def _initiate_parsing_process(self):
        """
        Do actual parsing process
        """

        # Clean date
        self.df['date'] = self.import_df[self.parser_dict['date_col']].apply(self.clean_date)
        

        
        

        # Clean title
        # self.import_df[self.parser_dict['title_col']] = self.import_df[self.parser_dict['title_col']].fillna(None)
        if self.parser_dict['title_fallback_col'] is None:
             self.df['title'] = self.import_df[self.parser_dict['title_col']].apply(self.clean_title)
        else:
            self.df['title'] = np.where(
                self.import_df[self.parser_dict['title_col']].notna(),
                self.import_df[self.parser_dict['title_col']].apply(self.clean_title),
                self.import_df[self.parser_dict['title_fallback_col']].apply(self.clean_title)
            )


        # Clean counterparty
        if self.parser_dict['counterparty_col'] is not None:
            # self.df['counterparty'] = self.import_df[self.parser_dict['counterparty_col']].apply(self.clean_title)
            if self.parser_dict['counterparty_fallback_col'] is not None:
                self.df['counterparty'] = np.where(
                    self.import_df[self.parser_dict['counterparty_col']].notna(),
                    self.import_df[self.parser_dict['counterparty_col']].apply(self.clean_title),
                    self.import_df[self.parser_dict['counterparty_fallback_col']].apply(self.clean_title),
                )
            else:
                self.import_df[self.parser_dict['counterparty_col']].apply(self.clean_title)
        else:
            self.df['counterparty'] = None

        
        # Clean IBAN and BIC text
        if self.parser_dict['iban_col'] is not None:
            self.import_df[self.parser_dict['iban_col']] = self.import_df[self.parser_dict['iban_col']].replace({np.nan: None})
            self.df['iban'] = self.import_df[self.parser_dict['iban_col']]
        else:
            self.df['iban'] = None

        if self.parser_dict['bic_col'] is not None:
            self.import_df[self.parser_dict['bic_col']] = self.import_df[self.parser_dict['bic_col']].replace({np.nan: None})
            self.df['bic'] = self.import_df[self.parser_dict['bic_col']]
        else:
            self.df['bic'] = None


        # Clean reference text
        if self.parser_dict['reference_text_col'] is not None:
            self.df['reference_text'] = self.import_df[self.parser_dict['reference_text_col']].apply(self.clean_title)
        else:
            self.df['reference_text'] = None


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
            self.df['spending_currency'] = np.where(
                self.df['spending_currency'].isna(),
                self.parser_dict['account_currency_default'],
                self.df['spending_currency']
            )


        
        # User currency
        self.df['user_currency'] = self.user.add_user_info.user_currency


        # Clean country
        if self.parser_dict['country_col'] is not None:
            self.import_df[self.parser_dict['country_col']] = self.import_df[self.parser_dict['country_col']].replace({np.nan: None})
            self.df['country'] = self.import_df[self.parser_dict['country_col']]
        else:
            self.df['country'] = None

        # Clean city
        if self.parser_dict['city_col'] is not None:
            self.import_df[self.parser_dict['city_col']] = self.import_df[self.parser_dict['city_col']].replace({np.nan: None})
            self.df['city'] = self.import_df[self.parser_dict['city_col']]
        else:
            self.df['city'] = None


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

        # Clean account amount
        self.df['account_amount'] = cleaned_account_amount

        # Clean spending amount
        self.df['spending_amount'] = cleaned_spending_amount

        # Fallback for spending amount to elimniate zeros
        if self.parser_dict['spending_amount_fallback_to_account_amount']:
            self.df['spending_amount'] = np.where(self.df['spending_amount'] == 0, self.df['account_amount'], self.df['spending_amount'])


        # Spending to account rate
        self.df['spending_account_rate'] = round(self.df['account_amount'] / self.df['spending_amount'], 8)


        # Account to user rate
        self.df['account_user_rate'] = self.df.apply(lambda row: FXRate.get_rate(date=row.date, transaction_currency=row.account_currency, counter_currency=self.user.add_user_info.user_currency), axis=1).astype(np.float64)
        
        
        # User amount
        self.df['user_amount'] = round(self.df['account_amount'] * self.df['account_user_rate'], 2)

        # Importing
        self.df['importing'] = self.importing.id

        # Account
        self.df['account'] = self.account.id

        # User
        self.df['user'] = self.user.id


        # create hash_duplicate key
        if self.parser_dict['hash_duplicate_col'] is None:
            
            # Create key with occs and assign to transaction
            self.df['all_cols'] = self.import_df.astype(str).values.sum(axis=1)
            self.df['cum_count'] = self.df.groupby('all_cols').cumcount().astype(str)
            key = self.df['all_cols'] + self.df['cum_count']
            self.df['hash_duplicate'] = key.apply(lambda item: hashlib.md5((item).encode('utf-8')).hexdigest())

        else:
            print('has hash_duplicate')
            self.df['hash_duplicate'] = self.import_df[self.parser_dict['hash_duplicate_col']]

        


    def parse(self):
        """
        Entry and exit method for APIParser
        :return: dict with parsed transactions
        """
        
        # read file or data in memory
        self.read_file()

        # to parsing
        self._initiate_parsing_process()

        # return parsed transactions for given account (returns dict)
        return self.df.to_dict('records')

    
    def save_csv(self, type):
        """
        :return: memory file
        """

        buf = StringIO()

        if type == 'raw':
            self.import_df.to_csv(buf, index=False)
        
        if type == 'parsed':
            self.df.to_csv(buf, index=False)

        buf.seek(0)

        return buf
