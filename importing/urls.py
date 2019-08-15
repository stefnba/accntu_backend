from django.urls import path

from .views import (
    ImportViaAPI,
    ImportViaAPIRunning,


    Test
)

app_name = "import_transaction"

urlpatterns = [
    path('import/api/', ImportViaAPI.as_view(), name='import-via-api'),
    path('import/api/running/<str:task_id>/', ImportViaAPIRunning.as_view(), name='import-via-api'),


    path('import/test/', Test.as_view(), name='import-test'),
]