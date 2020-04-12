from django.conf import settings
from django.db import models

from accounts.models import Account
from budget.models import Label, Expense
from business.models import Item
from importing.models import NewImportOneAccount


# Create your models here.


class FX(models.Model):
    date = models.DateField()
    transaction_currency = models.CharField(max_length=3)
    counter_currency = models.CharField(max_length=3)
    rate = models.DecimalField(decimal_places=8, max_digits=1000)

    def __str__(self):
        return '{}_{}_{}'.format(self.transaction_currency, self.counter_currency, self.date)

    class Meta:
        verbose_name = 'FX Rate'
        verbose_name_plural = 'FX Rates'



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
    importing = models.ForeignKey(NewImportOneAccount, on_delete=models.SET_NULL, blank=True, null=True)
    
    title = models.CharField(max_length=255)
    date = models.DateField()
    
    iban = models.CharField(max_length=255, blank=True, null=True)
    bic = models.CharField(max_length=255, blank=True, null=True)
    counterparty = models.CharField(max_length=255, blank=True, null=True)
    reference_text = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, blank=True, null=True) 
    # label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True, related_name='label')
    # tags
    status = models.CharField(choices=STATUS_CHOICES, max_length=10) 
    note = models.CharField(max_length=255, blank=True, null=True)

    spending_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    spending_currency = models.CharField(max_length=3)
    spending_account_rate = models.DecimalField(decimal_places=8, max_digits=1000)
    account_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    account_currency = models.CharField(max_length=3)
    account_user_rate = models.DecimalField(decimal_places=8, max_digits=1000)
    user_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    user_currency = models.CharField(max_length=3)   

    hash_duplicate = models.CharField(max_length=255) 
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) # only for odering
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'created_at']

    def __str__(self):
        return self.title


    # prev_category = None
    def __init__(self, *args, **kwargs):
        super(Transaction, self).__init__(*args, **kwargs)
        self.prev_category = self.category

    def save(self, *args, **kwargs):

        prev = str(self.prev_category).strip()
        current = str(self.category).strip()

        if current != prev:
            print('Change')

            # delete old private
            if prev == 'private':
                print('Delete old private')
                try:
                    instance = Expense.objects.get(pk=self.id)
                    instance.delete()
                except Expense.DoesNotExist:
                    print('item does not exist')
                    pass

            # create new private
            if current == 'private':
                print('Make new private')
                instance = Expense.objects.create(pk=self.id, budget_amount=self.user_amount)

            #  delete old business
            if prev == 'business':
                print('Delete old business')

                try:
                    instance = Item.objects.get(pk=self.id)
                    instance.delete()
                except Item.DoesNotExist:
                    pass

            #  create new business
            if current == 'business':
                instance = Item.objects.create(pk=self.id, report_amount=self.user_amount)


        super().save(*args, **kwargs)