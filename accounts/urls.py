from django.urls import path

from .views import (
    AccountList,
    AccountFullList,
)

app_name = "accounts"


urlpatterns = [
    path('', AccountList.as_view(), name='account-list'),
    path('full/', AccountFullList.as_view(), name='account_full-list'),
]