from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


# Create your models here.

def get_image_path(instance, filename):
    return 'providers/logos/{}/{}/{}'.format(instance.country, instance.key, filename)

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
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_type = models.CharField(max_length=255, choices=ACCESS_TYPE_CHOICES)
    provider_type = models.CharField(max_length=255, choices=PROVIDER_TYPE_CHOICES)
    currency = models.CharField(max_length=3)  
    import_details = models.ForeignKey('importing.ImportDetails', on_delete=models.SET_NULL, blank=True, null=True)

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
    first_import_success = models.BooleanField(default=False)
    sub_accounts_retrieved = models.BooleanField(default=False)
    last_import = models.DateTimeField(blank=True, null=True)


    login = models.CharField(max_length=255, blank=True, null=True)
    login_sec = models.CharField(max_length=255, blank=True, null=True)
    pin = models.CharField(max_length=255, blank=True, null=True)

    
    def __str__(self):
        return self.title


class Token_Data(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.CharField(max_length=255)
    host_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    expires_in = models.IntegerField()
    raw_token_data = JSONField()

    def __str__(self):
        return '{} - {}'.format(self.account, self.created_at)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Account Token Data'
        verbose_name_plural = 'Account Token Data'


class Sub_Account(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='sub_account')
    provider_subaccount_id = models.CharField(max_length=255, blank=True, null=True)
    provider_subaccount_name = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.provider_subaccount_name


    class Meta:
        verbose_name = 'Sub-Account'
        verbose_name_plural = 'Sub-Accounts'

