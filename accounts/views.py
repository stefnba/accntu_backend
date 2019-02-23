from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView
)

from .models import (
    Account
)

from .serializers import (
    AccountListSerializer,
    AccountFullListSerializer
)

# Create your views here.

"""
    Transactions
"""""""""""""""""""""""""""""""""""""""""""""

class AccountList(ListAPIView):
    " listing all account "
    
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer

class AccountFullList(ListAPIView):
    " listing all account with full information "
    
    queryset = Account.objects.all()
    serializer_class = AccountFullListSerializer
