from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


# Create your models here.

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
    bank = models.CharField(max_length=255)
    country = models.CharField(max_length=3)
    currency = models.CharField(max_length=3)
    mapping = JSONField()
    thousand_sep = models.CharField(max_length=1, blank=True, null=True, choices=DECIMAL_THOUSAND_CHOICES)
    decimal_sep = models.CharField(max_length=1, choices=DECIMAL_THOUSAND_CHOICES)
    has_negativesign = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title