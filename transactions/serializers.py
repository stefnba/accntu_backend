from rest_framework import serializers

from .models import (
    Transaction,
)

from accounts.models import Account

class AccountForTransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'title',)

class TransactionListSerializer(serializers.ModelSerializer):
    account = AccountForTransactionListSerializer(read_only=True) 
    
    class Meta:
        model = Transaction
        fields = (
            'id',
            'date',
            'title',
            'iban',
            'bic',
            'counterparty',
            'purpose',
            'country',
            'status',
            'note',
            'spending_amount',
            'spending_currency',
            'spending_account_rate',
            'account_amount',
            'account_currency',
            'account_user_rate',
            'user_amount',
            'user_currency',
            'account',
        )
        

    
class TransactionRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'title', 
            'iban', 
            'bic',
            'counterparty',
            'status',
        )
        read_only_fields = ('id', 'date')