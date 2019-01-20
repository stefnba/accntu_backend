from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4


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

class ProcessImport(object):
    def __init__(self, request):
        self.request = request
        self.hash_name = None
    
    # for future checks
    def get_filetype(self):
        return self.request.FILES['docfile'].content_type

    def get_user(self):
        return self.request.user.id

    def set_hash_name(self):
        hash_name = uuid4().hex[:20].upper()
        self.hash_name = hash_name
        return hash_name

    """ Methods called by view """
    def is_valid(self):
        serializer = FileImportSerializer(data=self.request.data)
        if serializer.is_valid():
            # override serializer and save instance to database
            serializer.save(
                        user_id=self.get_user(), 
                        hash_name=self.set_hash_name()
                    )
            return True
        return False

    def get_hash_name(self):
        return self.hash_name



class FileImport(APIView):
    """ Upload .csv file and save to respective folder in Media dir """
    
    parser_classes = (MultiPartParser, FormParser,)
    # serializer_class = ImportSerializer

    def put(self, request, format=None):

        import_transactions = ProcessImport(request)
        if import_transactions.is_valid():
            import_key = import_transactions.get_hash_name()
            return HttpResponse(import_key)
        else:
            return HttpResponseServerError()

    def get(self, equest, format=None):
        return Response('d')

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