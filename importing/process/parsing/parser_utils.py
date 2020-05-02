import requests
import pandas as pd
import numpy as np

from decimal import Decimal
from transactions.models import FX
from io import StringIO


def convert_upload_file(uploaded_file, account_id):
    """

    """
    

    # Check if csv
    try:
        uploaded_file.seek(0)
        file_text = str(uploaded_file.read().decode())

    except:
        
        # convert xls to csv
        try:
            buf = StringIO()
            file_df = pd.read_excel(uploaded_file)
            file_df.to_csv(buf, index=False, encoding='utf-8', sep=',')
            buf.seek(0)

            # get value of StringIO buf
            file_text = buf.getvalue()

        # return error if both csv and excel cannot be read
        except:
            return False

    return file_text


def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string


class FXRate(object):
    """
    Convert currency
    """
    
    FX_API_URL = 'https://api.exchangeratesapi.io/'
    
    
    def __init__(self, date, transaction_currency, counter_currency):

        self.date = date
        self.counter_currency = counter_currency
        self.transaction_currency = transaction_currency
        self.rate = None        

    # def get_amount(self, amount):
        
    #     amount = Decimal(amount) * Decimal(self.rate)
    #     return str(round(amount, 2))

    def retrieve_rate_from_db(self):
        try:
            pair = FX.objects.get(
                date=self.date, 
                counter_currency=self.counter_currency, 
                transaction_currency=self.transaction_currency
            )
            rate = pair.rate

            self.rate = float(rate)
            return rate

        except FX.DoesNotExist:
            return False
    
    def call_api(self):
        """
        Call api
        """

        r = requests.get('{}{}?base={}&symbols={}'.format(self.FX_API_URL, self.date, self.transaction_currency, self.counter_currency))
        
        if r.status_code == 200:
            res = r.json()

            rate = res.get('rates', None).get(self.counter_currency, None)

            # save rate to db
            save_rate = FX.objects.create(
                date=self.date,
                counter_currency=self.counter_currency, 
                transaction_currency=self.transaction_currency,
                rate=rate
            )

            # return rate
            return rate


        # return error
        return False


    
    @classmethod
    def get_rate(
        cls,
        date=None,
        transaction_currency=None,
        counter_currency=None
    ):
        """
        Get rate directly, e.g. for apply function in pandas df
        """

   
        # transaction currency equals counter currency
        if transaction_currency == counter_currency:
            return 1
        
        # fx conversion necessary
        else:
            converter = cls(date, transaction_currency, counter_currency)
            rate = converter.retrieve_rate_from_db()
            
            # rate already in db, no api call necessary
            if rate:
                return rate
            
            # query api if rate not available in db
            else:
                return converter.call_api()