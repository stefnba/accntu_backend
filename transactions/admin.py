from django.contrib import admin

# Register your models here.
from .models import (FX, Transaction)

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'date',
        'spending_amount',
        'spending_currency',
        'account_amount',
        'account_currency',
        'account',
    )

    list_filter = (
        'account',
        'spending_currency',
    )

admin.site.register(FX)
admin.site.register(Transaction, TransactionAdmin)

