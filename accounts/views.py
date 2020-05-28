from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)

from .models import (
    Account,
    Provider
)

from .serializers import (
    AccountListSerializer,
    AccountFullListSerializer,
    AccountRetrieveUpdateSerializer,
    ProviderListSerializer
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


class AccountCreate(CreateAPIView):
    """
    Create new accout
    """
    
    queryset = Account.objects.all()
    serializer_class = AccountRetrieveUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



"""
    Provider
"""""""""""""""""""""""""""""""""""""""""""""

class ProviderList(ListAPIView):
    """
    List all providers
    """
    
    queryset = Provider.objects.all()
    serializer_class = ProviderListSerializer