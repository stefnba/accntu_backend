from django.contrib import admin

# Register your models here.
from .models import (FX, Transaction, TransactionChangeLog)

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
        'spending_amount',
        'spending_currency',
        'account_amount',
        'account_currency',
        'account',
    )

    list_filter = (
        'account',
        'spending_currency',
        'status',
        'date',
        # 'user_amount'
    )

    search_fields = (
        'title',
    )

class FXAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'transaction_currency',
        'counter_currency',
        'rate'
    )

    list_filter = (
        'transaction_currency',
        'counter_currency',
        'date'
    )

    search_fields = (
        'date',
    )

admin.site.register(FX, FXAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionChangeLog)

