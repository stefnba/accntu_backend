from rest_framework import serializers
from ..models import (
    Transaction,
)

from accounts.serializers import AccountForTransactionSerializer


# Transaction One To One for budget and business
# ------------------------------------------------------------------------------

class TransactionOneToOneSerializer(serializers.ModelSerializer):
    """
    Fields from Transaction models for one to one relationship with Expense and Budget models
    """

    account = AccountForTransactionSerializer(read_only=True) 
    
    class Meta:
        model = Transaction
        fields = (
            'id',
            'title',
            'date',
            'account',
            'account_amount',
            'spending_amount',
            'spending_currency',
            'account_amount',
            'account_currency',
            'user_amount',
            'user_currency',
        )