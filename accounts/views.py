from celery.result import AsyncResult
from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import (
    Account,
    Provider
)

from .serializers import (
    AccountListSerializer,
    AccountFullListSerializer,
    AccountCreateRetrieveUpdateSerializer,
    ProviderListSerializer
)

from .tasks import test_connection

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


class AccountRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Retrieve and update single account
    """
    
    queryset = Account.objects.all()
    serializer_class = AccountCreateRetrieveUpdateSerializer
    lookup_field = 'id'


class AccountCreate(CreateAPIView):
    """
    Create new accout
    """
    
    queryset = Account.objects.all()
    serializer_class = AccountCreateRetrieveUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountTestConnect(APIView):
    """
    :post:
    """

    def post(Self, request):
        """
        Attempt to connect to provider
        """
        
        account_id = request.data.get('account', None)

        if account_id:
            
            # start import process in tasks.py
            task = test_connection.delay(
                account_id=account_id,
            )
            
            res = {
                'task_id': task.id,
                'res_msg': 'Import has started',
                'respone': 'IMPORT_STARTED'
            }

            return Response(res, status=status.HTTP_201_CREATED)
        
        return Response({
            'err_msg': 'Please provide account information!',
            'error': 'ACCOUNT_MISSING'
        }, status=status.HTTP_400_BAD_REQUEST)


class AccountTestConnectRunning(APIView):
    """
    Get status of running task based on task id
    """

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        res = {
            'state': task.state,
            'meta': task.info
        }

        return Response(res, status=status.HTTP_200_OK)


"""
    Provider
"""""""""""""""""""""""""""""""""""""""""""""

class ProviderList(ListAPIView):
    """
    List all providers
    """
    
    queryset = Provider.objects.all()
    serializer_class = ProviderListSerializer