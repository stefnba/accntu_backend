from django.conf import settings
from django.db import models

# Create your models here.





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