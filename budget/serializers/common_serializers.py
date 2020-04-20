from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from transactions.serializers.nested_serializers import TransactionOneToOneSerializer

from ..models import (
    Bucket,
    Expense,
    Label,
    Icon
)


# Icons
# ------------------------------------------------------------------------------

class IconListSerializer(serializers.ModelSerializer):
    """
    List all icons
    Also used as nested serializer for LabelListSerializer 
    """

    class Meta:
        model = Icon
        fields = (
            'id',
            'name',
            'icon_svg',
            'icon_object'
        )


# Buckets
# ------------------------------------------------------------------------------

class BucketListSerializer(serializers.ModelSerializer):
    """
    List all buckets
    Also used as nested serializer for LabelListSerializer
    """

    class Meta:
        model = Bucket
        fields = (
            'id',
            'title',
            'color',
        )


# Labels
# ------------------------------------------------------------------------------

class LabelListSerializer(serializers.ModelSerializer):
    """
    List all labels 
    """

    icon = IconListSerializer(read_only=True)
    bucket = BucketListSerializer(read_only=True)
    
    class Meta:
        model = Label
        fields = (
            'id',
            'title',
            'rank',
            'icon',
            'bucket'
        )






class LabelListAddInfoSerializer(serializers.ModelSerializer):
    """
    List all labels with additional information on sum and count 
    """
    """ Also used as nested serializer for BucketWithLabelsListSerializer """

    # transaction_count = serializers.SerializerMethodField()
    # transaction_sum = serializers.SerializerMethodField()
    icon = IconListSerializer(read_only=True)
    
    class Meta:
        model = Label
        fields = (
            'id',
            'title',
            'rank',
            'icon',
            # 'transaction_count',
            # 'transaction_sum',
        )


    # def get_transaction_count(self, obj):
    #     print(obj.label.all().aggregate(Sum('budget_amount')))
    #     return obj.label.count()

    # def get_transaction_sum(self, obj):
    #     s = obj.label.all().aggregate(Sum('budget_amount'))['budget_amount__sum']
    #     if s:
    #         return s
        
    #     return 0


class LabelRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Retrieve, update or destroy label
    """

    # icon = IconListSerializer(read_only=True)

    class Meta:
        model = Label
        fields = (
            'id',
            'title',
            'bucket',
            'icon'
        )


class LabelCreateSerializer(serializers.ModelSerializer):
    """
    Create new label
    """

    # icon = IconListSerializer(read_only=True)

    class Meta:
        model = Label
        fields = (
            'id',
            'title',
            'bucket',
            'icon'
        )


#  Buckets
###########################
    
class BucketWithLabelsListSerializer(serializers.ModelSerializer):
    """ List all buckets with list of associated labels """

    labels = LabelListAddInfoSerializer(read_only=True, source='bucket', many=True)

    class Meta:
        model = Bucket
        fields = (
            'id',
            'title', 
            'labels',
            'icon',
            'color'
        )


#  Expense
###########################

class ExpenseListSerializer(serializers.ModelSerializer):
    """  """

    label = LabelListSerializer(read_only=True)
    transaction = TransactionOneToOneSerializer(read_only=True)

    class Meta:
        model = Expense
        # fields = '__all__'
        fields = (
            'transaction',
            'budget_amount',
            'label',
        )
    
    # make items at same level as other serializer fields
    def to_representation(self, instance):
        data = super(ExpenseListSerializer, self).to_representation(instance)
        items = data.pop('transaction')

        for key, val in items.items():
            data.update({key: val})
        return data


#  Expense Bulk Update
###########################

class ExpenseBulkListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):

        print(instance)
        print(validated_data)

        # Maps for id->instance and id->data item.
        book_mapping = {book.transaction_id: book for book in instance}
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


class ExpenseBulkUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    # expense = ExpenseForTransactionListSerializer()

    class Meta:
        model = Expense
        fields = (
            'id',
            'label'
        )
        list_serializer_class = ExpenseBulkListSerializer




    



