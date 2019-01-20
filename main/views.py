from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView
)

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    FileImport,
    Transaction
)

from .serializers import (
    FileImportSerializer,
    TransactionListSerializer
)

from .utils.dd import Barclaycard


# Create your views here.


"""
    Import
"""""""""""""""""""""""""""""""""""""""""""""

class TransactionList(ListAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer


"""
    Transactions
"""""""""""""""""""""""""""""""""""""""""""""

class TransactionList(ListAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer



"""
    Test
"""""""""""""""""""""""""""""""""""""""""""""

class Test(APIView):
    def get(self, request):
        print('ddd')

        # barclaycard = Barclaycard(
        #     'sjb6211',
        #     'Jlup.com.66.Huu',
        #     '2013011016'
        # )

        # target_dir = './Import/'

        # if barclaycard.download_csv():
        #     barclaycard.move_download(target_dir)

        return Response('ff')