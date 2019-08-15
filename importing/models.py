from django.conf import settings
from django.db import models

# Create your models here.

class NewImport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['imported_at',]

    def __str__(self):
        return self.imported_at