from rest_framework import serializers

from .models import (
    Transaction,
)

"""
    Transaction
"""""""""""""""""""""""""""""""""""""""""""""

class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    
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