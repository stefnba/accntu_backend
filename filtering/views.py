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
    },
    'label': {
        'title': 'label__title'
    },
}


class Filtering(ListModelMixin, GenericAPIView):
    queryset = Transaction.objects.all()
    filterset_class = TransactionFilterSet

    def list(self, request, *args, **kwargs):


        print(Transaction.CATEGORY_CHOICES)


        qs = self.filter_queryset(self.get_queryset())

        fields = FILTER_FIELDS

        filter_options = {}

        for field in fields:
            qs_distinct = qs.order_by(field).values_list(field, flat=True).distinct(field)

            filter_choices = []
            
            for item in list(qs_distinct):

                title = item

                # if different title is specified
                add_info = FILTER_FIELDS_NESTED.get(field, None)
                if add_info is not None:
                
                    field_name = add_info.get('title', None)
                    field_value = qs.filter(**{ field: item }).values(field_name).first()
                    title = field_value[field_name]
                
                filter_choices.append({
                    'id': item,
                    'title': title
                })
            
            
            filter_options[field] = filter_choices

        
        return Response(filter_options)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
        