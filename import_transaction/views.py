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
from .utils.upload import ReadFromFile

# Create your views here.
import csv
from io import TextIOWrapper

import json

class Upload(APIView):

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user_id=request.user.id
            )

            # read .csv file
            file_request = request.FILES['upload_file']
            account = request.POST.get('account')

            read_file = ReadFromFile(file_request, account)
            if read_file.is_valid():
                return Response(read_file.get_data(), status=status.HTTP_200_OK)
            
            return Response(read_file.get_error(), status=status.HTTP_400_BAD_REQUEST)
        return Response(False)

class Import(ListCreateAPIView):

    def create(self, request, *args, **kwargs):

        transactions = request.data
        user = request.user.id

        serializer = ImportSerializer(data=transactions, many=True, context={'request': request})
        
        # print(serializer.initial_data)
        if serializer.is_valid():
            
            # save import to db
            account = serializer.validated_data[0]['account']
            import_record = ImportUpload.objects.create(
                user_id=user,
                account=account
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



"""
    Test
"""""""""""""""""""""""""""""""""""""""""""""

class Test(APIView):
    def get(self, request):
        
        print(request.user.id)
        return Response('request')


