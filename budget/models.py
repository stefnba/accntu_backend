from django.conf import settings
from django.db import models

# Create your models here.


class Bucket(models.Model):
    title = models.CharField(max_length=255)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['rank',]


class Label(models.Model):
    title = models.CharField(max_length=255)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Bucket, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ['id']


class Expense(models.Model):
    transaction = models.OneToOneField(to='transactions.Transaction', on_delete=models.CASCADE, primary_key=True)
    active = models.BooleanField(default=True)
    budget_amount = models.DecimalField(decimal_places=2, max_digits=1000, default=0)