from django.urls import path

from .views import (
    Import,
    ImportLocal,
    Upload,
    Test,
    Test2,
    Test4,


    ImportViaAPI,
    ImportViaAPIRunning,
)

app_name = "import_transaction"

urlpatterns = [
    path('import/', Import.as_view(), name='file-import'),
    path('upload/', Upload.as_view(), name='file-upload'),
    path('import/local/', ImportLocal.as_view(), name='file-upload'),
    path('test/', Test.as_view(), name='test'),
    path('test/<str:id>/', Test2.as_view(), name='test'),
    path('driver/', Test4.as_view(), name='test'),


    path('import/api/', ImportViaAPI.as_view(), name='import-via-api'),
    path('import/api/running/<str:task_id>/', ImportViaAPIRunning.as_view(), name='import-via-api'),
]