from django.contrib import admin

# Register your models here.
from .models import (
    NewImport,
    NewImportOneAccount,
)

admin.site.register(NewImport)
admin.site.register(NewImportOneAccount)