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
            'reference_text',
            'country',
            'category',
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
    # status_readable = serializers.CharField(source='get_status_display') # human-readable choice output
    # category_readable = serializers.CharField(source='get_category_display') # human-readable choice output

    # company_type_name = serializers.SerializerMethodField()
    # def get_company_type_name(self, obj):
    #     return obj.get_status_display()

    # gender = serializers.ChoiceField(choices=(('private','Private'),))


    class Meta:
        model = Transaction
        fields = (
            'id',
            'date',
            'title', 
            'iban', 
            'bic',
            'counterparty',
            'status',
            # 'status_readable',
            'category',
            # 'category_readable',
            'spending_amount',
            'spending_currency',
            'spending_account_rate',
            'account_amount',
            'account_currency',
            'account_user_rate',
            'user_amount',
            'user_currency',
            # 'company_type_name',
        )
        read_only_fields = (
            'id', 
            'date',
            'spending_amount',
            'spending_currency',
            'spending_account_rate',
            'account_amount',
            'account_currency',
            'account_user_rate',
            'user_amount',
            'user_currency',
            # 'status_readable',
            # 'category_readable',
        )



class TransactionBulkListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):

        # Maps for id->instance and id->data item.
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        return ret


class TransactionBulkUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'title',
            'category',
            'status',
        )
        list_serializer_class = TransactionBulkListSerializer