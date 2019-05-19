from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView
)

from transactions.models import (
    Transaction
)

from .models import (
    Item,
    Report,
)

from .serializers import (
    AssignableTransactionsListSerializer,
    ReportListSerializer,
    ReportItemRetrieveUpdateSerializer,
    ReportRetrieveUpdateSerializer,
)

# Create your views here.

class ReportListDraft(ListAPIView):
    """ listing all transactions """
    
    queryset = Report.objects.filter(status='draft')
    serializer_class = ReportListSerializer


class ReportListSubmitted(ListAPIView):
    """ listing all transactions """
    
    queryset = Report.objects.filter(status='submitted')
    serializer_class = ReportListSerializer


class AssignableTransactionsList(ListAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.filter(status='debit', category='business')
    serializer_class = AssignableTransactionsListSerializer


class TransactionRetrieveUpdate(RetrieveUpdateAPIView):
    """ listing all transactions """
    
    queryset = Report.objects.all()
    serializer_class = ReportRetrieveUpdateSerializer
    lookup_field = 'id'

class ItemRetrieveUpdate(RetrieveUpdateAPIView):
    """ Retrieve / update one report item """
    
    queryset = Item.objects.all()
    serializer_class = ReportItemRetrieveUpdateSerializer

