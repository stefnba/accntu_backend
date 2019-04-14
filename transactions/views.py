from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView
)

from django.db.models import Q

from django_filters import rest_framework as filters
from django_filters.fields import Lookup


from .models import (
    Transaction
)

from .serializers import (
    TransactionListSerializer,
    TransactionRetrieveUpdateSerializer,
)

from functools import reduce
from operator import and_

# Create your views here.

# class ListFilter(filters.Filter):
#     def filter(self, qs, value):
        
#         # if value is None:
#         #     return super(ListFilter, self).filter(qs, value)

#         value_list = value.split(u',')
#         # print(value_list)



#         return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))

# class ProductFilterSet(FilterSet):
#     # counterparty = ListFilter(field_name='counterparty')
#     # account = ListFilter(field_name='account')
#     account = NumberFilter(field_name='account')

#     class Meta:
#         model = Transaction
#         fields = ['account', ]


class ListFilter(filters.Filter):

    def customize(self, value):
        return value

    def filter(self, qs, value):

        multiple_vals = [7,8]
        i = Lookup( multiple_vals, "in")

        print(i)

        multiple_vals = map(self.customize, multiple_vals)
        actual_filter = Lookup(multiple_vals, 'in')

        print(actual_filter)

        return super(ListFilter, self).filter(qs, i)

class TransactionFilterSet(filters.FilterSet):
    # account = filters.NumberFilter(field_name='account')
    account = ListFilter(field_name='account')

    class Meta:
        model = Transaction
        fields = ['account',]


class TransactionList(ListAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer

    # filterset_class = TransactionFilterSet

    def get_queryset(self):
        
        # values = ["2019-02-28",'2019-03-02']

        # q_objects = Q()

        # f_name = 'date'

        # for item in values:
        #     q_objects.add(Q('{}={}'.format(f_name, item)), Q.OR)

        # queryset = Transaction.objects.filter(q_objects)


        #------


        params = self.request.query_params
        print(params)

        filters = {k: v.split(u',') for k, v in params.items()}

        # print(a)

        # filters = {'account': [6, 7, 8], 'date': ['2019-02-28']}

        queryset = Transaction.objects.filter(reduce(and_, (Q(**{f'{k}__in': v}) for k, v in filters.items())))



        #-----
        

        # questions = [('question__contains', 'test'), ('question__gt', 23 )]
        # q_list = [Q(x) for x in questions]
        # Poll.objects.filter(reduce(operator.or_, q_list))

        
        
        
        # params = self.request.query_params
        # # print(params)

        # for param in list(params.keys()):
        #     values = params.get(param, None)

        #     # print(values)

        #     # for value in values:
        #     #     print(param, value)

            

        return queryset


class TransactionRetrieveUpdate(RetrieveUpdateAPIView):
    """ listing all transactions """
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionRetrieveUpdateSerializer
    lookup_field = 'id'