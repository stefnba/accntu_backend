from django.contrib import admin

# Register your models here.
from .models import (
    Account,
    Provider,
    Sub_Account
)

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'provider',
        'user',
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(Provider)
admin.site.register(Sub_Account)