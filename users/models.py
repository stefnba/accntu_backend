
from django.conf import settings
from django.db import models

# Create your models here.

class Settings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    user_currency = models.CharField(max_length=3)