from django.urls import path

from .views import (
    TransactionBulkUpdate,
    TransactionList,
    TransactionRetrieveUpdate,
)

app_name = "transactions"


urlpatterns = [
    path('transaction/<int:id>/', TransactionRetrieveUpdate.as_view(), name='transaction-detail'),
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    path('transactions/update/', TransactionBulkUpdate.as_view(), name='transaction-bulk-update'),
]