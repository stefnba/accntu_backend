from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from importing.models import CsvXlsImportDetails

# Create your models here.

class Provider(models.Model):
    
    ACCESS_TYPE_CHOICES = (
        ('api','API Access'), 
        ('scr','Web Scrapping'),
        ("csv","CSV Import")
    )

    PROVIDER_TYPE_CHOICES = (
        ('card','Card'), 
        ('account','Account')
    )
    
    provider = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    country = models.CharField(max_length=2)
    color = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_type = models.CharField(max_length=255, choices=ACCESS_TYPE_CHOICES)
    provider_type = models.CharField(max_length=255, choices=PROVIDER_TYPE_CHOICES)
    currency = models.CharField(max_length=3)  
    csvxls_import = models.ForeignKey('importing.CsvXlsImportDetails', on_delete=models.SET_NULL, blank=True, null=True)

    parser_map = JSONField()
    csv_meta = JSONField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.provider, self.country)


class Account(models.Model):
    
    DECIMAL_THOUSAND_CHOICES = (
        ('.','.'), 
        (',',','),
        ("'","'")
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider,on_delete=models.SET_NULL, blank=True, null=True)
    provider_account_id = models.CharField(max_length=255, blank=True, null=True)


    login = models.CharField(max_length=255, blank=True, null=True)
    login_sec = models.CharField(max_length=255, blank=True, null=True)
    pin = models.CharField(max_length=255, blank=True, null=True)

    
    def __str__(self):
        return self.title


class Sub_Account(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    provider_subaccount_id = models.CharField(max_length=255, blank=True, null=True)
    provider_subaccount_name = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.provider_subaccount_name


    class Meta:
        verbose_name = 'Sub-Account'
        verbose_name_plural = 'Sub-Accounts'

