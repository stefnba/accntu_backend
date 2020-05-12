from django.contrib import admin

# Register your models here.
from .models import (
    Account,
    Provider,
    Sub_Account,
    Token_Data
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
admin.site.register(Token_Data)