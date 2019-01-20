from django.conf import settings
from django.db import models

from datetime import datetime
import os

# Create your models here.

"""
    Utils for Models
"""""""""""""""""""""""""""""""""""""""""""""

# Set path and filename of imported file
def user_dir_path(instance, filename):
    
    account = str(instance.account)
    dt = datetime.now()
    
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second

    ext = os.path.splitext(filename)[1:]
    filename_new = "{}_{}{:02d}{:02d}_{:02d}{:02d}{:02d}{}".format(
                                            account, 
                                            year, 
                                            month, 
                                            day, 
                                            hour, 
                                            minute, 
                                            second, 
                                            ext
                                        )

    return 'import/{}/{}/{:02d}/{}'.format(instance.user.id, year, month, filename_new)



"""
    Import
"""""""""""""""""""""""""""""""""""""""""""""
class FileImport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    # account = models.ForeignKey(Accounts, on_delete=models.SET_NULL, blank=True, null=True)
    hash_string = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    docfile = models.FileField(upload_to=user_dir_path)

    class Meta:
        ordering = ['uploaded_at',]

    def __str__(self):
        return self.docfile

"""
    Transaction
"""""""""""""""""""""""""""""""""""""""""""""
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    # account = models.ForeignKey(Accounts, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # import
    
    title = models.CharField(max_length=255)
    title_original = models.CharField(max_length=255)
    date = models.DateField()

    # status credit/debit
    # iban
    # bic
    
    # type private business none
    # tags
    # note 
    # category 

    spending_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    spending_curr = models.CharField(max_length=3)
    spending_account_rate = models.DecimalField(decimal_places=4, max_digits=1000)
    account_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    account_curr = models.CharField(max_length=3)
    account_user_rate = models.DecimalField(decimal_places=4, max_digits=1000)
    user_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    user_curr = models.CharField(max_length=3)    

    class Meta:
        ordering = ['date', 'created_at']

    def __str__(self):
        return self.name