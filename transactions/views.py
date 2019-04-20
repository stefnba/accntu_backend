from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView
)

from .models import (
    Transaction
)

from .serializers import (
    TransactionListSerializer,
    TransactionRetrieveUpdateSerializer,
)

from filtering.filters import TransactionFilterSet


# Create your views here.

class TransactionList(ListAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer

    filterset_class = TransactionFilterSet

    # def get_queryset(self):
    #     # filter queryset against url
    #     params = self.request.query_params
    #     print(params)
    #     filters = {k: v.split(u',') for k, v in params.items()}
    #     print(filters)
    #     return Transaction.objects.filter(reduce(and_, (Q(**{f'{k}__in': v}) for k, v in filters.items())))


class TransactionRetrieveUpdate(RetrieveUpdateAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionRetrieveUpdateSerializer
    lookup_field = 'id'