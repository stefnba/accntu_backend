from django.conf import settings
from django.db import models

from datetime import datetime
import os

from accounts.models import Account

# Create your models here.

class NewImport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    nmbr_transactions = models.IntegerField(blank=True, null=True)
    import_success = models.BooleanField(default=False)

    class Meta:
        ordering = ['imported_at',]
        verbose_name = 'Import'
        verbose_name_plural = 'Imports'

    def __str__(self):
        return str(self.imported_at)



# Set path and filename of imported csv file
def get_file_path(instance, filename):
    
    account = str(instance.account)
    dt = datetime.now()
    user = instance.user.id

    extension = os.path.splitext(filename)[1:]
    filename_new = "{}_{}{:02d}{:02d}_{:02d}{:02d}{:02d}{}".format(
                                            account, 
                                            dt.year, 
                                            dt.month, 
                                            dt.day, 
                                            dt.hour, 
                                            dt.minute, 
                                            dt.second, 
                                            extension
                                        )

    return 'imports/{}/{}/{:02d}/{}/{}'.format(user, dt.year, dt.month, account, filename_new)

class NewImportOneAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    nmbr_transactions = models.IntegerField(blank=True, null=True)
    new_import = models.ForeignKey(NewImport, on_delete=models.SET_NULL, blank=True, null=True)
    import_success = models.BooleanField(default=False)
    raw_csv = models.FileField(upload_to=get_file_path, blank=True, null=True)

    class Meta:
        ordering = ['imported_at',]
        verbose_name = 'Import per Account'
        verbose_name_plural = 'Imports per Account'

    def __str__(self):
        return str(self.imported_at)





# Set path and filename of photo TAN image
def get_image_path(instance, filename):
    
    account = str(instance.account)
    dt = datetime.now()
    user = instance.user.id

    extension = os.path.splitext(filename)[1:]
    filename_new = "{}_{}{:02d}{:02d}_{:02d}{:02d}{:02d}{}".format(
                                            account, 
                                            dt.year, 
                                            dt.month, 
                                            dt.day, 
                                            dt.hour, 
                                            dt.minute, 
                                            dt.second, 
                                            extension
                                        )

    return 'auth/photo_tan/{}/{}/{:02d}/{}'.format(user, dt.year, dt.month, filename_new)


class PhotoTAN(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    photo_tan = models.ImageField(upload_to=get_image_path)
    hash_url = models.CharField(max_length=255)