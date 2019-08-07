from django.contrib import admin

# Register your models here.
from .models import (
    Account,
    Provider
)

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'provider',
        'user',
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(Provider)