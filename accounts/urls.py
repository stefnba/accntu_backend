from django.urls import path

from .views import (
    AccountList,
    AccountFullList,
    AccountRetrieveUpdate,
)

app_name = "accounts"


urlpatterns = [
    path('', AccountList.as_view(), name='account-list'),
    path('full/', AccountFullList.as_view(), name='account_full-list'),
    path('account/<int:id>/', AccountRetrieveUpdate.as_view(), name='account-detail'),
]