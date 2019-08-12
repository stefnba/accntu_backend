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



from .tasks import do_work
from celery.result import AsyncResult


from pyvirtualdisplay import Display
from selenium import webdriver




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

            saved = serializer.save(
                user_id=user
            )

            saved = [t for t in saved if t is not False]
            res = {
                'transactions': 'to come',
                'nmbr': len(saved)
            }
            
            return Response(res, status=status.HTTP_201_CREATED)

        else:
            print('not valid')
            print(serializer.errors)

            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




""" 
    Test
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




class Test(APIView):
    def get(self, request):
        
        task = do_work.delay(45)
        print(task)
        print(f"id={task.id}, state={task.state}, status={task.status}") 
        print(task.get())
        return HttpResponse(task.id)



class Test2(APIView):
    def get(self, request, id):
        
        res = AsyncResult(id)
        print(res.state)
        print(res.get())
        return HttpResponse(res.get())


class Test4(APIView):
    def get(self, request):

        display = Display(visible=0, size=(800, 600))
        display.start()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        prefs={"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('https://www.google.com/')
        print(driver.title)
        driver.close()


        title = 12

        return HttpResponse(title)






