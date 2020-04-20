from rest_framework import serializers
from ..models import (
    Bucket,
    Expense,
    Label,
    Icon
)

#  Helpers
###########################


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






class ExpenseForTransactionBulkUpdateSerializer(serializers.ModelSerializer):
    """  """

    class Meta:
        model = Expense
        fields = (
            'budget_amount',
            'label',
        )