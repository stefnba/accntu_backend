from django.shortcuts import render

from rest_framework import status

from rest_framework.generics import (
    ListAPIView,
)

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.generics import (
    ListAPIView,
    GenericAPIView
)

from rest_framework.mixins import ListModelMixin

from transactions.models import (
    Transaction
)

from .filters import FILTER_FIELDS, TransactionFilterSet


# Create your views here.


FILTER_FIELDS_NESTED = {
    'account': {
        'title': 'account__title'
    }
}


class Filtering(ListModelMixin, GenericAPIView):
    queryset = Transaction.objects.all()
    filterset_class = TransactionFilterSet

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        fields = FILTER_FIELDS

        filter_options = {}

        for field in fields:
            value = qs.order_by(field).values_list(field, flat=True).distinct(field)

            add_info = FILTER_FIELDS_NESTED.get(field, None)
            
            if add_info is not None:
                v = []
                for item in list(value):

                    field_name = add_info.get('title', None)
                    field_value = qs.filter(account=item).values(field_name).first()
                
                    v.append({
                        'key': item,
                        'title': field_value[field_name]
                    })
                
                value = v
            
            filter_options[field] = value

        
        return Response(filter_options)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)



# class Filtering(APIView):

#     def get(self, request):

#         fields = (
#             'account__title',
#             'account_currency', 
#             'counterparty',
#             'country',
#             'date', 
#             'spending_currency', 
#             'status'
#         )

#         filter_options = {}

#         values = Transaction.objects.all()

#         for field in fields:
#             value = values.order_by(field).values_list(field, flat=True).distinct(field)
#             filter_options[field] = value

#         return Response(filter_options, status=status.HTTP_200_OK)


    # queryset = Transaction.objects.all()
    # serializer_class = DateListSerializer

    # def get_queryset(self):
    #     b = 'date'
    #     a = Transaction.objects.values_list(b, flat=True).distinct(b)
    #     print(list(a))
    #     print(len(list(a)))

    #     return Transaction.objects.distinct('date')

