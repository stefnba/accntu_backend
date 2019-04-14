from django.conf import settings
from django.db import models

from accounts.models import Account
from import_transaction.models import ImportUpload

# Create your models here.


class FX(models.Model):
    date = models.DateField()
    transaction_currency = models.CharField(max_length=3)
    counter_currency = models.CharField(max_length=3)
    rate = models.DecimalField(decimal_places=4, max_digits=1000)



class Transaction(models.Model):

    STATUS_CHOICES = (
        ('credit','credit'), 
        ('debit','debit'),
        ("transfer","transfer")
    )


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    import_upload = models.ForeignKey(ImportUpload, on_delete=models.SET_NULL, blank=True, null=True)
    
    title = models.CharField(max_length=255)
    date = models.DateField()
    
    iban = models.CharField(max_length=255, blank=True, null=True)
    bic = models.CharField(max_length=255, blank=True, null=True)
    counterparty = models.CharField(max_length=255, blank=True, null=True)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    
    # type private business none
    # tags
    # bucket 
    # business_report
    status = models.CharField(choices=STATUS_CHOICES, max_length=10) 
    note = models.CharField(max_length=255, blank=True, null=True)

    spending_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    spending_currency = models.CharField(max_length=3)
    spending_account_rate = models.DecimalField(decimal_places=4, max_digits=1000)
    account_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    account_currency = models.CharField(max_length=3)
    account_user_rate = models.DecimalField(decimal_places=4, max_digits=1000)
    user_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    user_currency = models.CharField(max_length=3)   

    hash_duplicate = models.CharField(max_length=255) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) # only for odering
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'created_at']

    def __str__(self):
        return self.title