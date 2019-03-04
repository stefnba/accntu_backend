# from django.http import HttpResponse, HttpResponseServerError
# from django.shortcuts import render
# from rest_framework.generics import (
#     ListAPIView
# )
# from rest_framework.parsers import FormParser, MultiPartParser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from uuid import uuid4


# from .models import (
#     Transaction
# )

# from .serializers import (
#     TransactionListSerializer
# )

# from .utils.dd import Barclaycard


# # Create your views here.

# """
#     Transactions
# """""""""""""""""""""""""""""""""""""""""""""

# class TransactionList(ListAPIView):
#     """ listing all transactions """
    
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionListSerializer



# """
#     Test
# """""""""""""""""""""""""""""""""""""""""""""

# class Test(APIView):
#     def get(self, request):
#         print(request.user.id)

#         # barclaycard = Barclaycard(
#         #     'sjb6211',
#         #     'Jlup.com.66.Huu',
#         #     '2013011016'
#         # )

#         # target_dir = './Import/'

#         # if barclaycard.download_csv():
#         #     barclaycard.move_download(target_dir)

#         return Response('request')