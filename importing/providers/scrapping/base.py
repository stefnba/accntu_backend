from django.core.files.base import ContentFile

from explicit import waiter, ID
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import urllib.parse as urlparse
import requests

from ...extracting.extractor import BaseExtractor
from ...models import NewImportOneAccount


class BaseScrapper(object):
    
    url = None
    skiprows = None
    sep = None  
    cutrows = 0

    def __init__(self):
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        prefs={"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)


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


    def quit_driver(self):
        self.driver.quit()


    def navigate(self):
        # placeholder method
        return True

    
    def pre_download(self):
        # placeholder method
        return {}


    def extend_period(self):
        # placeholder method
        return True


    def download_csv(self):
        pre = self.pre_download()

        url = pre.get('url', None)
        data = pre.get('data', None)
        params = pre.get('params', None)

        cookies = self.transfer_cookies()

        r = requests.post(url, data=data, params=params, cookies=cookies)
        csv = r.text

        # quite driver
        self.quit_driver()

        return csv


    def get_raw_transactions(self, **kwargs):

        print(kwargs)

        # navigate to download page
        self.navigate()

        # extend period
        extend = self.extend_period()
        if not extend:
            return []

        csv = self.download_csv()

        # save csv to db
        csv_file = ContentFile(str.encode(csv))

        c = NewImportOneAccount.objects.get(pk=kwargs['import_id'])
        c.raw_csv.save("text.csv", csv_file)

        csv_meta = kwargs.get('csv_meta', None)
        sep = csv_meta.get('sep', None)
        skiprows = csv_meta.get('skiprows', None)
        cutrows = csv_meta.get('cutrows', None)

        extracted = BaseExtractor(csv, sep, skiprows, cutrows)
        return extracted.return_extracted_transactions()
