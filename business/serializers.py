from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from transactions.models import (
    Transaction
)

from .models import (
    Item,
    Report,
)



#  Transaction
###########################

class TransactionOneToOneSerializer(serializers.ModelSerializer):
    """ Fields from Transaction models for one to one relationship with Item model """
    
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


#  Item
###########################

class ReportItemRetrieveUpdateSerializer(serializers.ModelSerializer):
    """ One single Item (business transaction), used for retrieve / update """

    class Meta:
        model = Item
        # fields = '__all__'
        fields = (
            'report_amount',
            'report',
            'has_system',
            'has_receipt',
        )


class ReportItemsListSerializer(serializers.ModelSerializer):
    """  """

    items = TransactionOneToOneSerializer(source='transaction', read_only=True)

    class Meta:
        model = Item
        # fields = '__all__'
        fields = (
            'report_amount',
            'report',
            'items',
            'has_system',
            'has_receipt',
        )
    
    # make items at same level as other serializer fields
    def to_representation(self, instance):
        data = super(ReportItemsListSerializer, self).to_representation(instance)
        items = data.pop('items')
        for key, val in items.items():
            data.update({key: val})
        return data


#  Report
###########################

class ReportListSerializer(serializers.ModelSerializer):
    """ List all Reports """

    report_total = serializers.DecimalField(decimal_places=2, max_digits=6)
    nmbr_items = serializers.IntegerField()

    class Meta:
        model = Report
        # fields = '__all__'
        fields = (
            'id',
            'title',
            'report_total',
            'submit_amount',
            'submit_date',
            'status',
            'nmbr_items',
            'start_date',
            'end_date',
        )


class ReportRetrieveUpdateSerializer(serializers.ModelSerializer):
    report_total = serializers.DecimalField(decimal_places=2, max_digits=6, read_only=True)
    nmbr_items = serializers.IntegerField(read_only=True)
    items = ReportItemsListSerializer(source='item', many=True, read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'title',
            'status',
            'start_date',
            'end_date',
            'submit_date',
            'submit_amount',
            'payout_date',
            'payout_amount',
            'nmbr_items',
            'report_total',
            'items',
        )

        read_only_fields = (
            'nmbr_items',
            'report_total',
            'items',
        )


class ReportCreateSerializer(serializers.ModelSerializer):
    """ Create new Report """

    def create(self, validated_data):
        user = self.context['request'].user
        return Report.objects.create(user=user, **validated_data)

    class Meta:
        model = Report
        # fields = '__all__'
        fields = (
            'title',
            'start_date',
            'end_date',
            'id'
        )




