from django.urls import path

from .views import (
    AccountList,
    AccountFullList,
    AccountRetrieveUpdateDestroy,
    AccountCreate,
    AccountTestConnect,
    AccountTestConnectRunning,
    ProviderList,
)

app_name = "accounts"


urlpatterns = [
    path('', AccountList.as_view(), name='account-list'),
    path('full/', AccountFullList.as_view(), name='account_full-list'),
    path('account/<int:id>/', AccountRetrieveUpdateDestroy.as_view(), name='account-detail-retrieve-update-destroy'),
    path('account/create/', AccountCreate.as_view(), name='account-create'),
    path('account/connect/', AccountTestConnect.as_view(), name='account-test-connect'),
    path('account/connect/<str:task_id>/', AccountTestConnectRunning.as_view(), name='account-test-connect-running-task'),
    path('providers/', ProviderList.as_view(), name='provider-list'),
]