import csv
import os
import time

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

class Barclaycard(object):

    DRIVER_PATH = './chromedriver'
    URL = 'https://banking.barclaycard.de/bir/feature/loginprocess'
    DOWNLOAD_DIR = './Downloads/latest/'
    TIMEOUT = 10

    def __init__(self, user, password, account):
        self.user = user
        self.password = password
        self.account = account

    def upload_csv(self):
        pass

    def download_csv(self):
        """ web scraping for Barclaycard """

        # pre-check if download dir exists, if not create
        if not os.path.isdir(self.DOWNLOAD_DIR):
            os.makedirs(self.DOWNLOAD_DIR)

        option = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : self.DOWNLOAD_DIR}
        option.add_experimental_option('prefs',prefs)
        # option.add_argument('--no-sandbox')
        option.add_argument('--window-size=1420,1080')
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')

        # start browser and get url
        browser = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=option)
        browser.get(self.URL)

        try:
            WebDriverWait(browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='loginTopImage']")))
        except TimeoutException:
            print('Timed out waiting for page to load')
            browser.quit()
        except:
            print('Login page could not be loaded')
            browser.quit()

        try: 
            browser.find_element_by_id('loginForm:loginName').send_keys(self.user)
            browser.find_element_by_id ('loginForm:password').send_keys(self.password)
            browser.find_element_by_id('loginForm:loginLink').click()
            
        except:
            print('Login not successful')

        # wait for post-login page to load
        try:
            WebDriverWait(browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//tbody[@id='j_id97:CreditCardTable:tbody_element']")))
            print('Login successful')
            
            # go to resp. account
            browser.find_element_by_partial_link_text(self.account).click()

        except TimeoutException:
            print('Timed out waiting for page to load')
            browser.quit()

        # wait for download link to load
        try:
            WebDriverWait(browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//td[@id='detailForm:j_id188']/div/a")))
        except TimeoutException:
            print('Timed out waiting for page to load')
            browser.quit()

        # Click on .csv Download link
        try:
            browser.find_elements_by_xpath("//td[@id='detailForm:j_id188']/div/a")[-1].click()
            print('File downloaded')
            
            # move and subsequently import downloaded .csv
            return True

        except IndexError:
            print('There was an error')

        return False
    
    def move_download(self, target_dir):
        """ Move file from web scraping download dir to import dir """

        # sleeper to get actual file and not download dummy
        time.sleep(2)
        
        # list files in download folder
        files = os.listdir(self.DOWNLOAD_DIR)
        
        # check if dir contains files
        if not files:
            print('ERROR: no files in dir')
            return False

        # get first file (there should only be one file)
        file = files[0]

        # pre-check if target dir exists, if not create
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        # delete unnecessary rows in file
        self.clean_file(self.DOWNLOAD_DIR, file)
        
        # rename file
        # Todo ---> rename file

        # move file
        os.rename(os.path.join(self.DOWNLOAD_DIR, file), os.path.join(target_dir, file))


    def clean_file(self, source_dir, file):
        """ Remove first rows of Barclaycard export which are not necessary 
            File is not moved with this function, so function can be used for any Barclaycard export """
       
       # delete how many rows
        n = 11

        file_loc = os.path.join(source_dir, file)
        
        try:
            # open file and read all rows
            with open(file_loc, 'r', encoding='mac_roman', newline='') as f:
                data = list(csv.reader(f, delimiter=',')) 

            with open(file_loc, 'w', encoding='mac_roman') as f:
                # delete rows in array, i.e. csv file
                del data[:n]
                
                # write new file
                writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in data:
                    writer.writerow(row)

            return True
        
        except:
            print('ERROR: there was an error cleaning the export')
            return False



# barclaycard = Barclaycard(
#     'sjb6211',
#     'Jlup.com.66.Huu',
#     '2013011016'
# )

# target_dir = './Import/'

# if barclaycard.download_csv():
#     barclaycard.move_download(target_dir)


