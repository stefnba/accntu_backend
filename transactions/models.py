from django.conf import settings
# from django.apps import apps
from django.db import models

from accounts.models import Account
from budget.models import Label, Expense
from import_transaction.models import ImportUpload
from business.models import Item


# Item = apps.get_model('business', 'Item')

# Create your models here.


class FX(models.Model):
    date = models.DateField()
    transaction_currency = models.CharField(max_length=3)
    counter_currency = models.CharField(max_length=3)
    rate = models.DecimalField(decimal_places=4, max_digits=1000)



class Transaction(models.Model):

    STATUS_CHOICES = (
        ('credit','Credit'), 
        ('debit','Debit'),
        ('transfer','Transfer')
    )

    CATEGORY_CHOICES = (
        ('private','Private'), 
        ('business','Business'),
    )


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    import_upload = models.ForeignKey(ImportUpload, on_delete=models.SET_NULL, blank=True, null=True)
    
    title = models.CharField(max_length=255)
    date = models.DateField()
    
    iban = models.CharField(max_length=255, blank=True, null=True)
    bic = models.CharField(max_length=255, blank=True, null=True)
    counterparty = models.CharField(max_length=255, blank=True, null=True)
    reference_text = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, blank=True, null=True) 
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True)
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
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) # only for odering
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'created_at']

    def __str__(self):
        return self.title


    prev_category = None
    def __init__(self, *args, **kwargs):
        super(Transaction, self).__init__(*args, **kwargs)
        self.prev_category = self.category

    def save(self, *args, **kwargs):

        # print('prev', self.prev_category, 'kk')
        # print('now', self.category)

        if self.prev_category is not self.category:
            print('changed')

            if self.prev_category is 'business':
                print('was b')

            if self.category is not 'business':
                print('delete')
                try:
                    instance = Item.objects.get(pk=self.id)
                    instance.delete()
                except Item.DoesNotExist:
                    pass
                

            if self.category is 'business':
                instance = Item.objects.create(pk=self.id, report_amount=self.user_amount)

            if self.category is 'private':
                instance = Expense.objects.create(pk=self.id, budget_amount=self.user_amount)

        super().save(*args, **kwargs)