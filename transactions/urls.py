from django.urls import path

from .views import (
    TransactionList,
)

app_name = "transactions"


urlpatterns = [
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
]