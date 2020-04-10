from django.contrib import admin

# Register your models here.
from .models import (
    NewImport,
    NewImportOneAccount,
    CsvXlsImportDetails,
    PhotoTAN
)

admin.site.register(NewImport)
admin.site.register(NewImportOneAccount)
admin.site.register(CsvXlsImportDetails)
admin.site.register(PhotoTAN)