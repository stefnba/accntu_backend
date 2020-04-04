from django.conf import settings
from django.db import models

import os

# Create your models here.

# Set path and filename of uploaded icon
def get_file_path(instance, filename):
    
    name = str(instance.name)
    extension = os.path.splitext(filename)[1:]
    filename_new = "{}{}".format(name, extension)

    return 'icons/{}'.format(filename_new)

class Icon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # icon = models.ImageField(upload_to=get_file_path)
    icon_object = models.TextField(blank=True, null=True)
    icon_svg = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return self.name

class Bucket(models.Model):
    title = models.CharField(max_length=255)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    icon = models.CharField(max_length=255)
    color = models.CharField(max_length=255)

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
    bucket = models.ForeignKey(Bucket, on_delete=models.SET_NULL, blank=True, null=True, related_name='bucket')
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, blank=True, null=True, related_name='icon')

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ['id']


class Expense(models.Model):
    transaction = models.OneToOneField(to='transactions.Transaction', on_delete=models.CASCADE, primary_key=True)
    active = models.BooleanField(default=True)
    budget_amount = models.DecimalField(decimal_places=2, max_digits=1000, default=0)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True, related_name='label')