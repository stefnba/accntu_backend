from celery import shared_task, current_task, task

from selenium import webdriver 
from explicit import waiter, ID
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select

import requests

import time



@task(bind=True)
def do_import(self, accounts):
    
    for account in accounts:
        print(account)















