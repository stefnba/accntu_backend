from celery import shared_task, current_task, task

from selenium import webdriver 
from explicit import waiter, ID
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

import requests

import time



@task(bind=True)
def do_import(self, accounts):
    pass



















def transfer_cookies(driver):
    driver_cookies = driver.get_cookies()
    cookies_copy = {}
    for driver_cookie in driver_cookies:
        cookies_copy[driver_cookie["name"]] = driver_cookie["value"]

    return cookies_copy


@shared_task
def do_work(list_of_work):

    


    for work_item in range(list_of_work):
        print(234234)
        return work_item
    return 'work is complete'


@shared_task
def adding_task(x, y):
    return x + y



@shared_task(bind=True)
def driver(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    prefs={"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chrome_options=chrome_options)


    url = 'https://www.miles-and-more.kartenabrechnung.de/'

    driver.get(url)


    try:
        waiter.find_write(driver, 'id104832590_j_username', '0310028305', by=ID)
        waiter.find_write(driver, 'id104832590_j_password', 'Kofk1203NAdsO&&$#!', by=ID, send_enter=True)

        self.update_state(state='PROGRESS',
                          meta={'status': 'looged in'})
    except:
        return False


    driver.get(url + 'mam/Home/content/FinancialStatus/Overview/main/Creditcard.xhtml?$event=showTransactions&id=0')
    

    self.update_state(state='PROGRESS',
                          meta={'status': 'navigated in'})

    select = waiter.find_element(driver, 'postingDate', by=By.NAME)
    select.clear()
    select.send_keys('01.01.2019')
    waiter.find_element(driver, 'button.evt-search', by=By.CSS_SELECTOR).click()


    waiter.find_element(driver, 'postingDate', by=By.NAME)

    cookies = transfer_cookies(driver)
    driver.close()

    
    r = requests.post('https://www.miles-and-more.kartenabrechnung.de/mam/Home/content/Creditcard/TransactionOverview.xhtml?$event=csvExport', cookies=cookies)
    return r.text
    # title = driver.title
    # driver.close()

    # return title




@task(bind=True)
def sleep_task(self, max):
    for i in range(100):
        time.sleep(1)
        
        

        self.update_state(state='PROGRESS',
                meta={'current': i, 'total': 100})


        print(i)