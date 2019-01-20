from django.urls import path

from .views import (
    FileImport,
    TransactionList,

    Test
)

app_name = "main"


urlpatterns = [

    # Import
    path('file_import/', FileImport.as_view(), name='file-import'),

    # Transactions
    path('transactions/', TransactionList.as_view(), name='transaction-list'),


    
    # Test
    path('test/', Test.as_view(), name='test'),
]