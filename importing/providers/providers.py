from explicit import waiter, ID
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
import requests

from .api.base import BaseApiAccess
from .scrapping.base import BaseScrapper


from django.core.cache import cache
import time

def wait_until(timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        tan_set = cache.ttl('my_key') # ttl not get since django-redis caching, async process on differnt memory
        print(tan_set)

        if tan_set:
            print('cache set')
            return True
        
        print('waiting')
        time.sleep(period)

    print('timeout')
    return False

class N26(BaseApiAccess):

    provider = 'n26'
    url = 'https://api.tech26.de'
    auth_endpoint = '/oauth/token'
    transactions_endpoint= '/api/smrt/transactions'


class MilesAndMore(BaseScrapper):

    provider = 'miles&more'
    url = 'https://www.miles-and-more.kartenabrechnung.de/'
    skiprows = 6
    sep = ';'


    def login(self, username, password):

        wait_until(30)

        try:
            self.driver.get(self.url)
            waiter.find_write(self.driver, 'id104832590_j_username', username, by=ID)
            waiter.find_write(self.driver, 'id104832590_j_password', password, by=ID, send_enter=True)

            return True
        except:
            return False


    def navigate(self):
        self.driver.get(self.url + 'mam/Home/content/FinancialStatus/Overview/main/Creditcard.xhtml?$event=showTransactions&id=0')

    
    def extend_period(self):
        select = waiter.find_element(self.driver, 'postingDate', by=By.NAME)
        select.clear()
        select.send_keys('01.01.2019')
        waiter.find_element(self.driver, 'button.evt-search', by=By.CSS_SELECTOR).click()


    def download(self):
        waiter.find_element(self.driver, 'postingDate', by=By.NAME)
        cookies = self.transfer_cookies()

        return self.request_csv(url='https://www.miles-and-more.kartenabrechnung.de/mam/Home/content/Creditcard/TransactionOverview.xhtml?$event=csvExport', cookies=cookies)



provider_classes = {
    'n26': N26,
    'miles&more': MilesAndMore,
}