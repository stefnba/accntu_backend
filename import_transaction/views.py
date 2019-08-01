from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import ImportUpload

from .serializers import (
    ImportSerializer,
    UploadSerializer
)
from .utils.upload import ExtractTransactions

# Create your views here.
import csv
from io import TextIOWrapper

import json







""" 
    Upload file and extract all transactions
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Upload(APIView):

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        serializer = UploadSerializer(data=request.data)

        # upload file
        if serializer.is_valid():
            upload = serializer.save(user_id=request.user.id)

            # read .csv file
            file_request = request.FILES['upload_file']
            account = request.POST.get('account')

            # extract transactions from file
            read_file = ExtractTransactions(file_request, account)

            # return if successful extraction
            if read_file.is_valid():
                context = {
                    'transactions': read_file.get_data(),
                    'upload': upload.id
                }

                return Response(context, status=status.HTTP_200_OK)
            
            return Response(read_file.get_errors(), status=status.HTTP_400_BAD_REQUEST)
       
       
        # return in case upload file serializer return false
        return Response(False)



""" 
    Save transactions to database
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Import(ListCreateAPIView):

    def create(self, request, *args, **kwargs):

        print(request.data)

        transactions = request.data.get('transactions', None)
        upload_file = request.data.get('upload', None)
        user = request.user.id

        if transactions is None or upload_file is None:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

        serializer = ImportSerializer(data=transactions, many=True, context={'request': request})
        
        if serializer.is_valid():
            
            # save import to db
            account = serializer.validated_data[0]['account']
            import_record = ImportUpload.objects.create(
                user_id=user,
                account=account,
                upload_file_id=upload_file
            )

            serializer.save(
                user_id=user,
                import_upload_id=import_record.id
            )

            return Response(True, status=status.HTTP_200_OK)
        else:
            print('not valid')
            # print(serializer.data)
            print(serializer.errors)

    
        return Response(True, status=status.HTTP_200_OK)




class ImportLocal(ListCreateAPIView):

    serializer_class = ImportSerializer
    queryset = ''
    
    def create(self, request, *args, **kwargs):

        transactions = request.data.get('transactions', None)
        user = request.user.id

        if transactions is None:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

        serializer = ImportSerializer(data=transactions, many=True, context={'request': request})

        if serializer.is_valid():
            print('valid')


            serializer.save(
                user_id=user,
            )

        else:
            print('not valid')
            print(serializer.errors)

        return Response(True, status=status.HTTP_200_OK)



""" 
    Test
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Test(APIView):
    def get(self, request):
        
        print(request.user.id)
        return Response('request')


