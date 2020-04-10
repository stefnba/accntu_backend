import requests

from decimal import Decimal

from transactions.models import FX

FX_API_URL = 'https://api.exchangeratesapi.io/'

class FXRate(object):
    def __init__(self, date, transaction_currency, counter_currency):

        self.date = date
        self.counter_currency = counter_currency
        self.transaction_currency = transaction_currency
        self.rate = None

    def get_rate(self):
        if self.transaction_currency == self.counter_currency:
            rate = 1
            self.rate = rate
            return str(rate)
        else:
            rate = self.retrieve_rate_from_db()

            print('rate', rate)
            
            if rate:
                # return rate if already in db
                return str(round(rate, 4))
            else:
                # do request if rate not available in db
                rate = self.call_api()

                # return rate for serializer
                if rate:
                    return str(round(rate, 4))
                
                return False
            

    def get_amount(self, amount):
        print(amount)
        print(self.rate)
        amount = Decimal(amount) * Decimal(self.rate)
        return str(round(amount, 2))

    def retrieve_rate_from_db(self):
        try:
            pair = FX.objects.get(
                date=self.date, 
                counter_currency=self.counter_currency, 
                transaction_currency=self.transaction_currency
            )
            rate = pair.rate

            self.rate = rate
            return rate

        except FX.DoesNotExist:
            return False
    
    def call_api(self):
        r = requests.get('{}{}?base={}&symbols={}'.format(FX_API_URL, self.date, self.transaction_currency, self.counter_currency))
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
            self.rate = rate
            return rate
        else:
            print(r.text)
            return False