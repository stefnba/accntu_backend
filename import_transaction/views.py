from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import UploadSerializer
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
                return Response(read_file.get_data(), status=status.HTTP_201_CREATED)
            
            return Response(read_file.get_error(), status=status.HTTP_400_BAD_REQUEST)
        return Response(False)


        # import_transactions = ProcessImport(request)
        # if import_transactions.is_valid():
        #     import_key = import_transactions.get_hash_name()
        #     return HttpResponse(import_key)
        # else:
        #     return HttpResponseServerError()


    # def get(self, request, format=None):
    #     return Response({'dd': 122}, status=status.HTTP_201_CREATED)



"""
    Test
"""""""""""""""""""""""""""""""""""""""""""""

class Test(APIView):
    def get(self, request):
        
        print(request.user.id)
        return Response('request')


