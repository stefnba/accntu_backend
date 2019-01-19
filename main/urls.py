from django.urls import path

from .views import (
    TransactionList,
)

app_name = "main"


urlpatterns = [
    
    # Transactions
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
]