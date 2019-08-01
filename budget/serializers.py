from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from transactions.models import (
    Transaction
)

from .models import (
    Expense,
)



#  Transaction
###########################

class TransactionOneToOneSerializer(serializers.ModelSerializer):
    """ Fields from Transaction models for one to one relationship with Expense model """
    
    class Meta:
        model = Transaction
        fields = (
            'id',
            'title',
            'date',
            'account_amount',
            'spending_amount',
            'spending_currency',
            'account_amount',
            'account_currency',
        )


#  Expense
###########################


class ExpenseListSerializer(serializers.ModelSerializer):
    """  """

    # transaction = TransactionOneToOneSerializer(source='transaction', read_only=True)
    transaction = TransactionOneToOneSerializer(read_only=True)

    class Meta:
        model = Expense
        # fields = '__all__'
        fields = (
            'budget_amount',
            'transaction',
        )
    
    # make items at same level as other serializer fields
    def to_representation(self, instance):
        data = super(ExpenseListSerializer, self).to_representation(instance)
        items = data.pop('transaction')

        # print(data)
        # print(self)

        for key, val in items.items():
            data.update({key: val})
        return data
