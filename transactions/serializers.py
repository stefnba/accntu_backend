from rest_framework import serializers

from .models import (
    Transaction,
)

from accounts.models import Account
from budget.models import (
    Bucket,
    Expense,
    Icon,
    Label,
)


#  Helpers
###########################

class AccountForTransactionListSerializer(serializers.ModelSerializer):
    """ Account helper for transaction list serializer """

    class Meta:
        model = Account
        fields = (
            'id',
            'title',
        )


class IconForTransactionListSerializer(serializers.ModelSerializer):
    """ Icon helper for transaction list serializer """

    class Meta:
        model = Icon
        fields = (
            'id',
            'icon_svg',
        )


class BucketForTransactionListSerializer(serializers.ModelSerializer):
    """ Bucket helper for transaction list serializer """

    class Meta:
        model = Bucket
        fields = (
            'id',
            'title',
            'icon',
            'color',
        )


class LabelForTransactionListSerializer(serializers.ModelSerializer):
    bucket = BucketForTransactionListSerializer(read_only=True) 
    icon = IconForTransactionListSerializer(read_only=True) 
    
    class Meta:
        model = Label
        fields = (
            'id',
            'title',
            'bucket',
            'icon'
        )

    # def to_representation(self, instance):
    #     data = super(LabelForTransactionListSerializer, self).to_representation(instance)

    #     bucket = data.pop('bucket')

    #     # if label has no bucket
    #     if bucket is None:
    #         return data

    #     for key, val in bucket.items():
    #         # use 'bucket' as key is tile and is already used for label
    #         data.update({'bucket': val})
    #     return data


class ExpenseForTransactionListSerializer(serializers.ModelSerializer):
    """  """

    label = LabelForTransactionListSerializer(read_only=True) 

    class Meta:
        model = Expense
        fields = (
            'budget_amount',
            'label',
        )


#  Transaction
###########################

class TransactionListSerializer(serializers.ModelSerializer):
    """ List all transactions """

    account = AccountForTransactionListSerializer(read_only=True) 
    expense = ExpenseForTransactionListSerializer(read_only=True) 
    
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
            'is_new',
            'expense',
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
        transaction_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # print(transaction_mapping)

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = transaction_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        return ret


class ExpenseForTransactionBulkUpdateSerializer(serializers.ModelSerializer):
    """  """

    class Meta:
        model = Expense
        fields = (
            'budget_amount',
            'label',
        )

class TransactionBulkUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    expense = ExpenseForTransactionBulkUpdateSerializer()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'title',
            'category',
            'status',
            'is_new',
            'expense',
        )
        list_serializer_class = TransactionBulkListSerializer

    def to_internal_value(self, data):
        return data


    def update(self, instance, validated_data):

        print(validated_data)


        expense_data = validated_data.pop('expense')

        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)
        instance.status = validated_data.get('status', instance.status)

        try:
            expense = instance.expense
            
            expense.label_id = expense_data.get(
                'label',
                expense.label_id
            )
            expense.budget_amount = expense_data.get(
                'budget_amount',
                expense.budget_amount
            )
            
            expense.save()

        except:
            pass

        instance.save()

        return instance



# Transaction One To One for budget and business
# ------------------------------------------------------------------------------

class TransactionOneToOneSerializer(serializers.ModelSerializer):
    """ Fields from Transaction models for one to one relationship with Expense and Budget models """

    account = AccountForTransactionListSerializer(read_only=True) 
    
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