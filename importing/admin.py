from django.contrib import admin

# Register your models here.
from .models import (
    NewImport,
    NewImportOneAccount,
    CsvXlsImportDetails,
    PhotoTAN,
    Upload
)


class ImportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'imported_at',
        # 'nmbr_transactions',
    )

    list_filter = (
        'user',
    )

class ImportOneAccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'imported_at',
        'account',
        'nmbr_transactions',
    )

    list_filter = (
        'user',
        'account',
    )


admin.site.register(NewImport, ImportAdmin)
admin.site.register(NewImportOneAccount, ImportOneAccountAdmin)
admin.site.register(CsvXlsImportDetails)
admin.site.register(PhotoTAN)
admin.site.register(Upload)