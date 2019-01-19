from django.shortcuts import render

from rest_framework.generics import ListAPIView


from .models import (
    Transaction
)

from .serializers import (
    TransactionListSerializer
)



# Create your views here.



"""
    Transactions
"""""""""""""""""""""""""""""""""""""""""""""
class TransactionList(ListAPIView):
    """ listing all transactions """
    
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer