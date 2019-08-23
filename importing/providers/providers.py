from django.core.files import File
from django.core.cache import cache

from explicit import waiter, ID
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

import requests
import tempfile
import time

from .api.base import BaseApiAccess
from .scrapping.base import BaseScrapper
from ..models import PhotoTAN

from .scrapping.utils import hash_url


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

    def login(self, username, password, login_sec):

        try:
            self.driver.get(self.url)
            waiter.find_write(self.driver, 'id104832590_j_username', username, by=ID)
            waiter.find_write(self.driver, 'id104832590_j_password', password, by=ID, send_enter=True)
            
            # TODO check element on next page
            return True

        except:
            return False

    def navigate(self):
        self.driver.get(self.url + 'mam/Home/content/FinancialStatus/Overview/main/Creditcard.xhtml?$event=showTransactions&id=0')

    
    def extend_period(self):
        try:
            select = waiter.find_element(self.driver, 'postingDate', by=By.NAME)
            select.clear()
            select.send_keys('01.01.2019')
            waiter.find_element(self.driver, 'button.evt-search', by=By.CSS_SELECTOR).click()

            # wait for page to reload
            waiter.find_element(self.driver, 'postingDate', by=By.NAME)
            
            return True
        
        except:
            print('period could not be extended')
            return False


    def pre_download(self):
        return {
            'url': 'https://www.miles-and-more.kartenabrechnung.de/mam/Home/content/Creditcard/TransactionOverview.xhtml?$event=csvExport'
        }


class DeutscheBank(BaseScrapper):

    provider = 'db'
    url = 'https://meine.deutsche-bank.de/'
    skiprows = 4
    sep = ';'
    cutrows = 1

    def login(self, username, password, login_sec):

        try:
            self.driver.get(self.url)
            waiter.find_write(self.driver, 'branch', login_sec, by=ID)
            waiter.find_write(self.driver, 'account', username, by=ID)
            waiter.find_write(self.driver, 'pin', password, by=ID, send_enter=True)
            
            # TODO check element on next page
            return True

        except:
            return False


    def login_two_factor(self, user, account):

        img_el = waiter.find_element(self.driver, '//div[@id="photoTANGraphic"]/div/img', by=By.XPATH)
        src = img_el.get_attribute('src')

        cookies = self.transfer_cookies()

        r = requests.get(src, cookies=cookies)

        img_name = src.split('/')[-1]
        temp_img = tempfile.NamedTemporaryFile()

        for block in r.iter_content(1024 * 8):
            # If no more file then stop
            if not block:
                break
                
            # Write image block to temporary file
            temp_img.write(block)


        hashed = hash_url(user, account, time.time())
        
        photo_tan = PhotoTAN()
        photo_tan.user_id = user
        photo_tan.account_id = account
        photo_tan.hash_url = hashed
        photo_tan.photo_tan.save(img_name, File(temp_img))

        return hashed


    def login_two_factor_submit_tan(self, tan):

        waiter.find_write(self.driver, 'tan', tan, by=By.NAME, send_enter=True)

        return True



    def navigate(self):
        waiter.find_element(self.driver, '00 persönliches Konto', by=By.PARTIAL_LINK_TEXT).click()
        

    
    def extend_period(self):
        waiter.find_write(self.driver, 'periodStartYear', '2018',  by=By.NAME)
        waiter.find_element(self.driver, '//form[@id="accountTurnoversForm"]/div[@class="formAction"]/span/input', by=By.XPATH).click()
        return True


    def pre_download(self):
        
        csv_link = waiter.find_element(self.driver, '//li[@class="csv"]/a', by=By.XPATH)
        csv_url = csv_link.get_attribute('href')
        
        return {
            'url': csv_url
        }



   




provider_classes = {
    'n26': N26,
    'miles&more': MilesAndMore,
    'db': DeutscheBank,
}