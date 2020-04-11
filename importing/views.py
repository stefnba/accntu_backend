from celery.result import AsyncResult
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .tasks import do_import
from .models import NewImportOneAccount, PhotoTAN
from django.core.files import File

import requests
import tempfile

from io import StringIO, BytesIO

from .providers.scrapping.utils import hash_url


from decouple import config
from pusher import Pusher


# Create your views here.

class ImportViaAPI(APIView):
    """
    GET: List all importable accounts for given user
    POST: Initiate new import process for provided accounts
    """

    def get(self, request):
        """
        List all importable accounts for given user
        """
        
        # TODO list all api and scrapping accounts here

        accounts = [1, 2, 3]
        
        return Response(accounts, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Initiate new import process for provided accounts
        If account list and user is provided, do_import in tasks.py is called
        and task_id is returned for view ImportViaAPIRunning
        """

        accounts = request.data.get('accounts', None)
        user = request.user.id

        # TODO remove here
        # accounts = [14]
        accounts = [18]
        user = 1

        if accounts and user:
            # start import process in tasks.py
            task = do_import.delay(accounts=accounts, user=user)
            
            res = {
                'task_id': task.id,
                'res_msg': 'Import has started',
                'respone': 'IMPORT_STARTED'
            }

            # return task id -> can be queried with view ImportViaAPIRunning
            return Response(res, status=status.HTTP_201_CREATED)

        return Response({
            'err_msg': 'No accounts provided!',
            'error': 'NO_ACCOUNTS'
        }, status=status.HTTP_400_BAD_REQUEST)



class ImportViaAPIRunning(APIView):
    """
    Get status of running task based on task id
    """

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        res = {
            'state': task.state,
            'meta': task.info
        }

        return Response(res, status=status.HTTP_201_CREATED)



class ImportViaAPITwoFactorSubmitTAN(APIView):

    def post(self, request):

        tan = request.data.get('tan', None)
        account = request.data.get('account', None)
        task_id = request.data.get('task', None)
        user = request.user.id

        print(tan, account, task_id, user)

        if tan and account and task_id and user:
            key = '{}_{}_{}'.format(user, account, task_id)
            cache.set(key, tan)

            res = {
                'msg': 'TAN successfully submitted',
                'task_id': task_id,
            }

            return Response(res, status=status.HTTP_201_CREATED)

        
        return Response({
            'err_msg': 'No TAN provided!'
        }, status=status.HTTP_400_BAD_REQUEST)


class ImportViaAPITwoFactorRetrievePhotoTAN(APIView):

    def get(self, request, hash_url):
        try:
            img = PhotoTAN.objects.get(hash_url=hash_url).photo_tan

            return HttpResponse(img, content_type="image/png")

        except:
            return Response({
                'err_msg': 'Photo TAN not found!'
            }, status=status.HTTP_400_BAD_REQUEST)


class Upload(APIView):

    def post(self, request):

        uploaded_file = request.FILES['file']
        account_id = request.data.get('id', None)
        user = request.user.id

        # Set to file position zero
        uploaded_file.seek(0)

        # TODO Convert XLS to CSV

        if user and account_id and uploaded_file:

            try:
                file_text = str(uploaded_file.read().decode())
            
            except:
                return Response({
                    'err_msg': 'Please provide a .CSV file',
                    'error': 'WRONG_DATA_TYPE'
                }, status=status.HTTP_400_BAD_REQUEST)


            # start import process in tasks.py
            print('start task')
            task = do_import.delay(
                accounts=[account_id],
                user=user,
                data=file_text,
                import_upload_type='upload'
            )

            res = {
                'task_id': task.id,
                'res_msg': 'Upload has started',
                'respone': 'UPLOAD_STARTED'
            }

            # return task id -> can be queried with view ImportViaAPIRunning
            return Response(res, status=status.HTTP_201_CREATED)
        

        return Response({
            'err_msg': 'Please provide all necessary information!',
            'error': 'DATA_MISSING'
        }, status=status.HTTP_400_BAD_REQUEST)










class Test(APIView):

    def get(self, request):

        # account_id = 14

        # qs = Account.objects.get(id=account_id)

        # parser_dict = qs.provider.csvxls_import.__dict__


        # account = {
        #     'account_id': account_id,
        #     'account_name': 'Barclaycard'
        # }
        
        # # p = Parser(parser_dict=parser_dict, file='importing/Barclaycard.xlsx', account=account)
        # p = ParserNew(parser_dict=parser_dict, file='importing/M&M.csv', account=account)
        # data_parsed = p.parse()
        
        
        # print(data_parsed)
        return Response('txt', status=status.HTTP_201_CREATED)
        

