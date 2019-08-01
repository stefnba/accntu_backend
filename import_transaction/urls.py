from django.urls import path

from .views import (
    Import,
    ImportLocal,
    Upload
)

app_name = "import_transaction"

urlpatterns = [
    path('import/', Import.as_view(), name='file-import'),
    path('upload/', Upload.as_view(), name='file-upload'),
    path('import/local/', ImportLocal.as_view(), name='file-upload'),
]