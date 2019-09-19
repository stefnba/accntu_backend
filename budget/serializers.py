from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault


from transactions.serializers import TransactionOneToOneSerializer

from .models import (
    Bucket,
    Expense,
    Label,
    Icon
)
from django.db.models import Sum


#  Icons
###########################

class IconListSerializer(serializers.ModelSerializer):
    """ List all icons """
    """ Also used as nested serializer for LabelListSerializer and  """

    class Meta:
        model = Icon
        fields = (
            'id',
            'name',
            'icon_svg',
            'icon_object'
        )


#  Labels
###########################

class LabelListSerializer(serializers.ModelSerializer):
    """ List all labels """
    """ Also used as nested serializer for BucketWithLabelsListSerializer """

    transaction_count = serializers.SerializerMethodField()
    transaction_sum = serializers.SerializerMethodField()
    icon = IconListSerializer(read_only=True)
    
    class Meta:
        model = Label
        fields = ('id', 'title', 'rank', 'icon', 'transaction_count', 'transaction_sum', )


    def get_transaction_count(self, obj):
        print(obj.label.all().aggregate(Sum('user_amount')))
        return obj.label.count()

    def get_transaction_sum(self, obj):
        s = obj.label.all().aggregate(Sum('user_amount'))['user_amount__sum']
        if s:
            return s
        
        return 0


class LabelRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """ Retrieve, update or destroy label """

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
    """ Create new label """

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

    labels = LabelListSerializer(read_only=True, source='bucket', many=True)

    class Meta:
        model = Bucket
        fields = ('id', 'title', 'labels', 'icon', 'color')


class BucketListSerializer(serializers.ModelSerializer):
    """ List all buckets """

    class Meta:
        model = Bucket
        fields = ('id', 'title',)






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

        for key, val in items.items():
            data.update({key: val})
        return data
