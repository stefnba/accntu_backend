from rest_framework import serializers

from budget.serializers.nested_serializers import (
    ExpenseForTransactionListSerializer,
    ExpenseForTransactionBulkUpdateSerializer,
)

from accounts.serializers import AccountForTransactionSerializer

from ..models import (
    Transaction,
    TransactionChangeLog,
)


#  Transaction
###########################

class TransactionListSerializer(serializers.ModelSerializer):
    """
    List all transactions
    """

    account = AccountForTransactionSerializer(read_only=True) 
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
    """

    """
    # status_readable = serializers.CharField(source='get_status_display') # human-readable choice output
    # category_readable = serializers.CharField(source='get_category_display') # human-readable choice output

    # company_type_name = serializers.SerializerMethodField()
    # def get_company_type_name(self, obj):
    #     return obj.get_status_display()

    # gender = serializers.ChoiceField(choices=(('private','Private'),))


    account = AccountForTransactionSerializer(read_only=True) 


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
            'account',
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
            'reference_text',
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
    """

    """

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




class TransactionBulkUpdateSerializer(serializers.ModelSerializer):
    """

    """

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

        UPDATEABLE_FILEDS = (
            'title',
            'category',
            'status',
            'expense__label_id',
        )

        updated_fields = []

        # update each field that is returned from e.g. form via dict validated_data
        for (key, value) in validated_data.items():

            # escape if fields is not allowed to be updated, continue with next in loop
            if key not in UPDATEABLE_FILEDS:
                continue
            

            # update nested
            if '__' in key:

                related_field, related_nested_field = key.split('__')
                

                # get nested instance
                try:
                    nested_instance = getattr(instance, related_field)

                except:
                    print('{} has no nested instance'.format(key))
                    continue


                # get field from nested instance
                try: 
                    prev_value = getattr(nested_instance, related_nested_field)
                except:
                    print('Nested instance has no related field')
                    prev_value = None


                # update value in db
                setattr(nested_instance, related_nested_field, value)
                nested_instance.save()
            
            else:
                try:

                    prev_value = getattr(instance, key)
                        
                    setattr(instance, key, value)
                    instance.save()

                except:
                    pass

        
            # only when values are different
            if prev_value != value:
                updated_fields.append({
                    'field': key, 
                    'updated_value': value,
                    'prev_value': prev_value
                })

            print(updated_fields)

        
        # # save
        # try:
        #     nested_instance.save()
        # except:
        #     pass

        # try:
        #     instance.save()
        # except:
        #     pass
        

        # add entry to change log db
        TransactionChangeLog.objects.bulk_create([ 
            TransactionChangeLog(**q, **{'transaction': instance, 'user': instance.user }) for q in updated_fields
        ])

        return instance