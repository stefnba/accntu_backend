from celery.result import AsyncResult
from django.core.cache import cache
from django.core.files import File
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
)

from accounts.models import Account
from .tasks import initiate_import
from .models import NewImport, NewImportOneAccount, PhotoTAN, Upload as NewUpload
from .serializers import ImportListSerializer

import requests
import tempfile

from io import StringIO, BytesIO

from .providers.scrapping.utils import hash_url


# Create your views here.

class ImportViaAPI(APIView):
    """
    :GET: List all importable accounts for given user
    :POST: Initiate new import process for provided accounts
    """

    def get(self, request):
        """
        List all importable accounts for given user
        """
        
        accounts = Account.objects.filter(
                provider__access_type__in=['api']
            ).values_list('id', flat=True)

        res = {
            'results': accounts,
        }
        
        return Response(res, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Initiate new import process for provided accounts
        If account list and user is provided, function initiate_import in tasks.py is called
        and task_id is returned for view ImportViaAPIRunning
        :return: task_id that can be queried with view ImportViaAPIRunning or error
        """

        accounts = request.data.get('accounts', None)
        user = request.user.id

        # TODO remove here
        # accounts = [14]
        # accounts = [18]
        accounts = [20]
        user = 1

        if accounts and user:
            
            # start import process in tasks.py
            task = initiate_import.delay(
                accounts=accounts,
                user=user
            )
            
            res = {
                'task_id': task.id,
                'res_msg': 'Import has started',
                'respone': 'IMPORT_STARTED'
            }

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
    """

    """

    def get(self, request, hash_url):
        try:
            img = PhotoTAN.objects.get(hash_url=hash_url).photo_tan

            return HttpResponse(img, content_type="image/png")

        except:
            return Response({
                'err_msg': 'Photo TAN not found!'
            }, status=status.HTTP_400_BAD_REQUEST)


class Upload(APIView):
    """

    """

    def post(self, request):

        uploaded_file = request.FILES['file']
        account_id = request.data.get('id', None)
        user = request.user.id

        if user and account_id and uploaded_file:

            # TODO Validate file type
            # if not file_text:
            #     return Response({
            #         'err_msg': 'Please provide a valid file',
            #         'error': 'WRONG_DATA_TYPE'
            #     }, status=status.HTTP_400_BAD_REQUEST)

            # save new upload to database
            new_upload = NewUpload.objects.create(
                user_id=user,
                account_id=account_id,
                upload_file=uploaded_file
            )

            # start import process in tasks.py
            print('start task')
            task = do_import.delay(
                accounts=[account_id],
                user=user,
                upload=new_upload.id,
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




class ImportList(ListAPIView):
    """
    List all imports with # transactions >0 done by a user
    """

    queryset = NewImport.objects.filter(nmbr_transactions__gt=0)
    serializer_class = ImportListSerializer

    # filterset_class = TransactionFilterSet


class Test(APIView):
    """
    Test View
    """

    def get(self, request):


        t = 10
        
        return Response(t, status=status.HTTP_201_CREATED)
        

