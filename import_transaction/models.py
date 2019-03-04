from django.conf import settings
from django.db import models

from accounts.models import Account

from datetime import datetime
import os

# Create your models here.

# Set path and filename of imported file
def file_dir_path(instance, filename):
    
    account = str(instance.account)
    dt = datetime.now()

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

    return 'import/{}/{}/{:02d}/{}'.format(instance.user.id, dt.year, dt.month, filename_new)



class FileUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload_file = models.FileField(upload_to=file_dir_path)

    class Meta:
        ordering = ['uploaded_at',]

    def __str__(self):
        return self.upload_file.name

class ImportUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    upload_file = models.ForeignKey(FileUpload, on_delete=models.SET_NULL, blank=True, null=True)
    