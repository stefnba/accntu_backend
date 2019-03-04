from django.urls import path

from .views import (
    TransactionList,
)

app_name = "transactions"


urlpatterns = [
    path('', TransactionList.as_view(), name='transaction-list'),
]