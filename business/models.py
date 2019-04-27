from django.conf import settings
from django.db import models

# Create your models here.



class Report(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    submit_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title',]