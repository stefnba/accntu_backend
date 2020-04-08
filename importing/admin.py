from django.contrib import admin

# Register your models here.
from .models import (
    NewImport,
    NewImportOneAccount,
    CsvXlsImportDetails
)

admin.site.register(NewImport)
admin.site.register(NewImportOneAccount)
admin.site.register(CsvXlsImportDetails)