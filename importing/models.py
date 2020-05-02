from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

from .utils.models_utils import (
    get_file_path,
    get_image_path,
    get_upload_file_path,
)

# from accounts.models import Account

# Create your models here.


class ImportDetails(models.Model):

    DATE_FORMAT_CHOICES = (
            ('%d.%m.%Y','%d.%m.%Y'), 
            # ('%d.%m.%y', str(datetime.now('%d.%m.%y'))), 
            ('%d.%m.%y', '11.03.20'), 
            ('timestamp_ms', 'timestamp_ms'), 
            ('timestamp', 'timestamp'), 
        )

    TYPE_CHOICES = (
        ('xls','XLS'), 
        ('csv','CSV'),
        ('dict','DICT'),
    )

    CSV_SEP_CHOICES = (
        (',',','), 
        (';',';'),
    )

    NUMBER_SEP_CHOICES = (
        ('.','.'), 
        (',',','),
        ('\'','\''),
    )

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # File info 
    file_type = models.CharField(choices=TYPE_CHOICES, max_length=10, blank=True, null=True) 
    csv_sep = models.CharField(choices=CSV_SEP_CHOICES, max_length=1, blank=True, null=True) 
    skiprows = models.IntegerField(default=0)
    cutrows = models.IntegerField(default=0)
    file_encoding = models.CharField(max_length=10, blank=True, null=True) 
    cols_to_drop = ArrayField(models.CharField(max_length=255, blank=True), blank=True, null=True)

    # Date
    date_col = models.CharField(max_length=255, blank=True, null=True) 
    date_format = models.CharField(choices=DATE_FORMAT_CHOICES, max_length=255, blank=True, null=True) 

    # Title
    title_col = models.CharField(max_length=255, blank=True, null=True) 
    title_fallback_col = models.CharField(max_length=255, blank=True, null=True) 

    # Country
    country_col = models.CharField(max_length=255, blank=True, null=True) 
    city_col = models.CharField(max_length=255, blank=True, null=True) 

    # Status
    status_col = models.CharField(max_length=255, blank=True, null=True) 
    status_col_map = JSONField(blank=True, null=True)
    account_amount_col_has_status = models.BooleanField(default=False)

    # Account currency
    account_currency_default = models.CharField(max_length=255, blank=True, null=True) 
    account_currency_col = models.CharField(max_length=255, blank=True, null=True) 
    account_amount_col_has_currency = models.BooleanField(default=False)

    # Spending currency
    spending_currency_col = models.CharField(max_length=255, blank=True, null=True) 
    spending_amount_col_has_currency = models.BooleanField(default=False)
    spending_currency_fallback_to_account_currency = models.BooleanField(default=False)


    # Account amount
    account_amount_col = models.CharField(max_length=255, blank=True, null=True) 
    account_amount_thousand_sep = models.CharField(choices=NUMBER_SEP_CHOICES, max_length=1, blank=True, null=True) 
    account_amount_decimal_sep = models.CharField(choices=NUMBER_SEP_CHOICES, max_length=1, blank=True, null=True) 

    # Spending amount
    spending_amount_col = models.CharField(max_length=255, blank=True, null=True) 
    spending_amount_fallback_to_account_amount = models.BooleanField(default=False)
    spending_amount_thousand_sep = models.CharField(choices=NUMBER_SEP_CHOICES, max_length=1, blank=True, null=True) 
    spending_amount_decimal_sep = models.CharField(choices=NUMBER_SEP_CHOICES, max_length=1, blank=True, null=True) 


    # IBAN & BIC
    iban_col = models.CharField(max_length=255, blank=True, null=True) 
    bic_col = models.CharField(max_length=255, blank=True, null=True) 


    # Reference text
    reference_text_col = models.CharField(max_length=255, blank=True, null=True) 
    reference_text_fallback_col = models.CharField(max_length=255, blank=True, null=True) 


    # Counterparty
    counterparty_col = models.CharField(max_length=255, blank=True, null=True)
    counterparty_fallback_col = models.CharField(max_length=255, blank=True, null=True) 


    # Hash key
    hash_duplicate_col = models.CharField(max_length=255, blank=True, null=True) 


    class Meta:
        ordering = ['name',]
        verbose_name = 'Import Details'
        verbose_name_plural = 'Import Details'

    def __str__(self):
        return str(self.name)



class NewImport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    nmbr_transactions = models.IntegerField(blank=True, null=True)
    import_success = models.BooleanField(default=False)

    class Meta:
        ordering = ['-imported_at',]
        verbose_name = 'Import'
        verbose_name_plural = 'Imports'

    def __str__(self):
        return str(self.imported_at)


class NewImportOneAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)
    nmbr_transactions = models.IntegerField(blank=True, null=True)
    new_import = models.ForeignKey(NewImport, on_delete=models.SET_NULL, blank=True, null=True)
    import_success = models.BooleanField(default=False)
    raw_csv = models.FileField(upload_to=get_file_path, blank=True, null=True)
    parsed_csv = models.FileField(upload_to=get_file_path, blank=True, null=True)

    class Meta:
        ordering = ['-imported_at',]
        verbose_name = 'Import per Account'
        verbose_name_plural = 'Imports per Account'

    def __str__(self):
        return str(self.imported_at)


class PhotoTAN(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    photo_tan = models.ImageField(upload_to=get_image_path)
    hash_url = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Photo TAN'
        verbose_name_plural = 'Photo TANs'


class Upload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload_file = models.FileField(upload_to=get_upload_file_path, blank=True, null=True)