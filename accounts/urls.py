from django.urls import path

from .views import (
    AccountList,
    AccountFullList,
    AccountRetrieveUpdate,
    AccountCreate,
    ProviderList,
)

app_name = "accounts"


urlpatterns = [
    path('', AccountList.as_view(), name='account-list'),
    path('full/', AccountFullList.as_view(), name='account_full-list'),
    path('account/<int:id>/', AccountRetrieveUpdate.as_view(), name='account-detail'),
    path('account/create/', AccountCreate.as_view(), name='account-create'),
    path('providers/', ProviderList.as_view(), name='provider-list'),
]