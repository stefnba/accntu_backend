

1)  View ImportViaAPI start import process via do_import in task.py
2)  Task do_import uses threads to retrieve transactions for all provided accounts
3)  


x)  Thread retrieve_account_transactions populates list importable_transactions
x)  ImportSerializer uses transactions in importable_transactions and saves those do database


do_import @ tasks.py    starts entire process


Scrapper @              gets raw csv data from web scrapping

Parser                  uses panda (for every given account)
                        - save raw csv
                        - parse csv/xls
                        - save parsed csv
                        - return parsed transactions