from django.urls import path

from .views import (
    Upload
)

app_name = "main"


urlpatterns = [

    # Import
    path('upload/', Upload.as_view(), name='file-import'),

]