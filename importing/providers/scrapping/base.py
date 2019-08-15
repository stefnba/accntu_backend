from explicit import waiter, ID
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import urllib.parse as urlparse
import requests

from ...extracting.extractor import BaseExtractor


class BaseScrapper(object):
    
    url = None
    skiprows = None
    sep = None  

    def __init__(self, username, password):
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        prefs={"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)
        
        
        
        # self.driver = webdriver.Chrome(executable_path=r'chromedriver')

        login = self.login(username, password)
        if login:
            self.navigate()
            self.extend_period()
            self.t = self.download()
        else:
            print('Login not successful')
            self.quit()


    


    def transfer_cookies(self):
        driver_cookies = self.driver.get_cookies()
        cookies_copy = {}
        for driver_cookie in driver_cookies:
            cookies_copy[driver_cookie["name"]] = driver_cookie["value"]

        return cookies_copy


    def get_current_url(self):
        return self.driver.current_url


    def get_url_params(self):
        url = self.get_current_url()
        parsed =  urlparse.urlparse(url)
        return urlparse.parse_qs(parsed.query)


    def request_csv(self, url=None, data=None, cookies=None, params=None):
        r = requests.post(url, data=data, params=params, cookies=cookies)
        return r.text

    def return_transactions(self):
        
        # TODO CSV EXTRACTION 
        t = self.t

        self.quit()

        extracted = BaseExtractor(t, self.sep, self.skiprows)

        # print(extracted.return_extracted_transactions())

        return extracted.return_extracted_transactions()


    def quit(self):
        self.driver.quit()
