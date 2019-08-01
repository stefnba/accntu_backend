from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render

from rest_framework.generics import (
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView
)

from .models import (
    Item,
    Report,
)

from transactions.models import (
    Transaction
)

from .serializers import (
    ReportCreateSerializer,
    ReportListSerializer,
    ReportItemsListSerializer,
    ReportItemRetrieveUpdateSerializer,
    ReportRetrieveUpdateSerializer,
    TransactionOneToOneSerializer,
)

# Create your views here.


#  Report
###########################

class ReportList(ListAPIView):
    """ listing all transactions """
    
    serializer_class = ReportListSerializer

    def get_queryset(self):
        print(self.kwargs['status'])
        return Report.objects.filter(status=self.kwargs['status'])


class ReportRetrieveUpdate(RetrieveUpdateAPIView):
    """ listing all transactions """
    
    queryset = Report.objects.all()
    serializer_class = ReportRetrieveUpdateSerializer
    lookup_field = 'id'


class ReportCreate(CreateAPIView):
    """" Create a new report """

    queryset = Report.objects.all()
    serializer_class = ReportCreateSerializer


class ReportDestroy(DestroyAPIView):
    """" Delete a report """

    queryset = Report.objects.all()
    serializer_class = ReportRetrieveUpdateSerializer
    lookup_field = 'id'





#  Item
###########################

class ItemRetrieveUpdate(RetrieveUpdateAPIView):
    """ Retrieve / update one report item """
    
    queryset = Item.objects.all()
    serializer_class = ReportItemRetrieveUpdateSerializer


class ItemListFilteredByReport(ListAPIView):
    """ listing all items, filtered by report """
    
    serializer_class = ReportItemsListSerializer

    def get_queryset(self):
        f = self.kwargs.get('report', None)        
        return Item.objects.filter(report=f).order_by('transaction__date', 'transaction_id')