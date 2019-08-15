from celery.result import AsyncResult
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .tasks import do_import

# Create your views here.

class ImportViaAPI(APIView):

    def get(self, request):
        
        # TODO list all api and scrapping accounts here

        accounts = [1, 2, 3]
        
        return Response(accounts, status=status.HTTP_200_OK)

    def post(self, request):

        accounts = request.data.get('accounts', None)
        user = request.user.id

        if accounts:
            task = do_import.delay(accounts, user)


            res = {
                'task_id': task.id,
                'msg': 'Import has started'
            }

            return Response(res, status=status.HTTP_201_CREATED)

        return Response({
            'err_msg': 'No accounts provided!'
        }, status=status.HTTP_400_BAD_REQUEST)


class ImportViaAPIRunning(APIView):

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        print(task)

        res = {
            'state': task.state,
            'meta': task.info
        }

        return Response(res, status=status.HTTP_201_CREATED)





class Test(APIView):

    def get(self, request):

        tan_set = cache.get('my_key')
        print(tan_set)

        cache.set('my_key', 'hello, world!', 30)

        tan_set = cache.get('my_key')
        print(tan_set)

        return Response("set", status=status.HTTP_200_OK)

