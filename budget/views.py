from django.db.models import Sum, Prefetch
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView

from rest_framework.response import Response
from filtering.filters import ExpenseFilterSet, TransactionFilterSet

from transactions.models import Transaction
from .models import (
    Bucket,
    Expense,
    Label,
    Icon,
)

from .serializers.common_serializers import (
    BucketListSerializer,
    BucketWithLabelsListSerializer,
    ExpenseListSerializer,
    IconListSerializer,
    LabelListSerializer,
    LabelRetrieveUpdateDestroySerializer,
    LabelCreateSerializer,
    ExpenseBulkUpdateSerializer,
)

# Create your views here.





# Create your views here.

class BudgetTransactionList(ListAPIView):
    """ listing all all private transactions that are debit """
    
    queryset = Expense.objects.filter(transaction__status='debit').order_by("-transaction__date")
    serializer_class = ExpenseListSerializer
    filterset_class = ExpenseFilterSet

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        total = queryset.aggregate(Sum('budget_amount'))['budget_amount__sum']

        response_data = {
            'stats': {
                'total': total if total else 0,
                'count': len(serializer.data),
            },
            'transactions': serializer.data
        }

        return Response(response_data)




class BucketsWithLabelsList(ListAPIView):
    """ listing all buckets with related Labels """
    
    queryset = Bucket.objects.prefetch_related(Prefetch('bucket', queryset=Label.objects.select_related('icon')))
    # queryset = Bucket.objects.all()
    # queryset = Bucket.objects.prefetch_related('bucket', 'bucket__icon')
    serializer_class = BucketWithLabelsListSerializer


class BucketsList(ListAPIView):
    """ listing all buckets """
    
    queryset = Bucket.objects.all()
    serializer_class = BucketListSerializer


class LabelCreate(CreateAPIView):
    """ create new label """
    
    queryset = Label.objects.all()
    serializer_class = LabelCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, rank=1)

class LabelRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """ retrieve, update or destroy label """
    
    queryset = Label.objects.all()
    serializer_class = LabelRetrieveUpdateDestroySerializer


class LabelList(ListAPIView):
    """ list all labels """
    
    queryset = Label.objects.all()
    serializer_class = LabelListSerializer


class IconList(ListAPIView):
    """ listing all buckets """
    
    queryset = Icon.objects.all()
    serializer_class = IconListSerializer


class IconRetrive(APIView):
    """ Get single icon by name """

    def get(self, request, pk):
        try:
            img = Icon.objects.get(pk=pk).icon_svg

            return HttpResponse(img, content_type="image/svg+xml")

        except:
            return Response({
                'err_msg': 'Photo TAN not found!'
            }, status=status.HTTP_400_BAD_REQUEST)


# Expense
###########################

class ExpenseBulkUpdate(APIView):

    def post(self, request, format=None):
        queryset = Expense.objects.all()
        serializer = ExpenseBulkUpdateSerializer(queryset, data=request.data, many=True, partial=True)
        if serializer.is_valid():
            saved = serializer.save()
            return Response({
                'length': len(saved)
            },  status=status.HTTP_201_CREATED)
        
        return Response('Update failed', status=status.HTTP_400_BAD_REQUEST)




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
