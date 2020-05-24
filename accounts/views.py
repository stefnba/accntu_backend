from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView
)

from .models import (
    Account
)

from .serializers import (
    AccountListSerializer,
    AccountFullListSerializer,
    AccountRetrieveUpdateSerializer
)

# Create your views here.

"""
    Accounts
"""""""""""""""""""""""""""""""""""""""""""""

class AccountList(ListAPIView):
    """
    List all account with nested provider info
    TODO Filter for active accounts only
    """
    
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer



class AccountFullList(ListAPIView):
    """
    Listing all account with full information
    """
    
    queryset = Account.objects.all()
    serializer_class = AccountFullListSerializer


class AccountRetrieveUpdate(RetrieveUpdateAPIView):
    """
    Retrieve and update single account
    """
    
    queryset = Account.objects.all()
    serializer_class = AccountRetrieveUpdateSerializer
    lookup_field = 'id'