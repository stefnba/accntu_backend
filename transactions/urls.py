from django.urls import path

from .views import (
    TransactionRetrieveUpdate,
    TransactionList,
)

app_name = "transactions"


urlpatterns = [
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    path('transaction/<int:id>/', TransactionRetrieveUpdate.as_view(), name='transaction'),
]