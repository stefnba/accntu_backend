from django.urls import path

from .views import (
    BucketsList,
    BucketsWithLabelsList,
    BudgetTransactionList,
    LabelCreate,
    LabelList,
    LabelRetrieveUpdateDestroy,
    IconRetrive,
    IconList,
)

app_name = "budget"


urlpatterns = [
    
    # Expenses
    path('expenses/', BudgetTransactionList.as_view(), name='expense-list'),
    
    # Labels
    path('labels/create/', LabelCreate.as_view(), name='label-create'),
    path('labels/', LabelList.as_view(), name='label-list'),
    path('labels/<int:pk>/', LabelRetrieveUpdateDestroy.as_view(), name='label-retrieve-update-destroy'),

    # buckets
    path('buckets/', BucketsList.as_view(), name='bucket-list'),
    path('buckets/labels/', BucketsWithLabelsList.as_view(), name='bucket-labels-list'),
    
    # icons
    path('icons/', IconList.as_view(), name='icon-list'),
    path('icons/<str:name>/', IconRetrive.as_view(), name='icon-retrieve'),
]