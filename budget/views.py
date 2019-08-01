from django.db.models import Sum
from django.shortcuts import render
from rest_framework.generics import (
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.response import Response

from .models import (
    Expense,
)

from .serializers import (
    ExpenseListSerializer,
)

# Create your views here.




# Expense
###########################


class BudgetListFilteredByPeriod(ListAPIView):
    """ listing all budget transactions from relevant period """
    
    queryset = Expense.objects.all()
    serializer_class = ExpenseListSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        distinct_dates = list(queryset.values_list('transaction__date', flat=True).distinct('transaction__date'))

        res_data = []
        for date in distinct_dates:
            transactions = queryset.filter(transaction__date=date)
            s = self.get_serializer(transactions, many=True)
            res_data.append({
                'date': date,
                'count': len(s.data),
                'daily_total': transactions.aggregate(Sum('budget_amount'))['budget_amount__sum'],
                'transactions': s.data,
            })

        return Response({
            'count': len(queryset),
            'total': queryset.aggregate(Sum('budget_amount'))['budget_amount__sum'],
            'transactions': res_data,
        })

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)

        # print(serializer)
