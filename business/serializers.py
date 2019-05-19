from rest_framework import serializers

from transactions.models import (
    Transaction
)

from .models import (
    Item,
    Report,
)

class ReportListSerializer(serializers.ModelSerializer):
    report_total = serializers.DecimalField(decimal_places=2, max_digits=6)
    nmbr_items = serializers.IntegerField()

    
    class Meta:
        model = Report
        # fields = '__all__'
        fields = (
            'id',
            'title',
            'report_total',
            'submit_date',
            'status',
            'nmbr_items',
            'start_date',
            'end_date',
        )




class AssignableTransactionsListSerializer(serializers.ModelSerializer):
    
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

class ReportItemRetrieveUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        # fields = '__all__'
        fields = (
            'report_amount',
            'report',
        )
    

class ReportItemsListSerializer(serializers.ModelSerializer):
    items = AssignableTransactionsListSerializer(source='transaction', read_only=True)

    class Meta:
        model = Item
        # fields = '__all__'
        fields = (
            'report_amount',
            'report',
            'items',
        )
    
    # make items at same level as other serializer fields
    def to_representation(self, instance):
        data = super(ReportItemsListSerializer, self).to_representation(instance)
        items = data.pop('items')
        for key, val in items.items():
            data.update({key: val})
        return data


class ReportRetrieveUpdateSerializer(serializers.ModelSerializer):
    report_total = serializers.DecimalField(decimal_places=2, max_digits=6)
    nmbr_items = serializers.IntegerField()
    items = ReportItemsListSerializer(source='item', many=True, read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'title',
            'report_total',
            'submit_date',
            'status',
            'nmbr_items',
            'start_date',
            'end_date',
            'items',
        )

        read_only_fields = (
            'nmbr_items',
            'report_total',
            'items',
        )