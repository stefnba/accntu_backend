from django.shortcuts import render

from rest_framework import status

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Transaction
)

from .serializers import (
    TransactionBulkUpdateSerializer,
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


class TransactionBulkUpdate(APIView):

    def post(self, request, format=None):
        queryset = Transaction.objects.all()
        serializer = TransactionBulkUpdateSerializer(queryset, data=request.data, many=True, partial=True)
        if serializer.is_valid():
            saved = serializer.save()
            return Response({
                'length': len(saved)
            },  status=status.HTTP_201_CREATED)
        
        return Response('Update failed', status=status.HTTP_400_BAD_REQUEST)

