from django.urls import path

from .views import (
    Filtering,
)

app_name = "filtering"


urlpatterns = [
    path('options/', Filtering.as_view(), name='filter-options'),
]