from django.urls import path

from .views import (
    Import,
    Upload
)

app_name = "main"

urlpatterns = [
    path('import/', Import.as_view(), name='file-import'),
    path('upload/', Upload.as_view(), name='file-upload'),
]