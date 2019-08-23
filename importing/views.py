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

from .providers.scrapping.utils import hash_url


from decouple import config
from pusher import Pusher


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
            }

            return Response(res, status=status.HTTP_201_CREATED)

        return Response({
            'err_msg': 'No accounts provided!'
        }, status=status.HTTP_400_BAD_REQUEST)


class ImportViaAPIRunning(APIView):

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












class Test(APIView):

    def get(self, request):
        

        txt = """Buchungstag;Wert;Umsatzart;Beg¸nstigter / Auftraggeber;Verwendungszweck;IBAN;BIC;Kundenreferenz;Mandatsreferenz ;Gl‰ubiger ID;Fremde Geb¸hren;Betrag;Abweichender Empf‰nger;Anzahl der Auftr‰ge;Anzahl der Schecks;Soll;Haben;W‰hrung
12.08.2019;12.08.2019;"Kartenzahlung";;YUM 2 TAKE//Muenchen/DE 09-08-2019T13:06:00 Folgenr. 09 Verfalld. 1223;;;;;;;;;;;-13,80;;EUR
12.08.2019;12.08.2019;"SEPA-‹berweisung an";Stefan Jakob Bauer (N26);Transferred with Deutsche Bank Mobile;DE24100110012627811735;NTSBDEB1XXX;;;;;;;;;-1.000,00;;EUR
12.08.2019;12.08.2019;"SEPA-‹berweisung an";Stefan """

        # txt = '12.08.2019;12.08.2019'




        myfile = ContentFile(str.encode(txt))
            


        a = NewImportOneAccount()
        a.user_id = 1
        a.account_id = 10

        a.raw_csv.save("text.csv", myfile)

        # a = NewImportOneAccount.objects.create(user_id=1, account_id=10, raw_csv=f)

        return Response(txt, status=status.HTTP_201_CREATED)
        
