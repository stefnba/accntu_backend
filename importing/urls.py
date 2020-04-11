from django.urls import path

from .views import (
    ImportViaAPI,
    ImportViaAPIRunning,
    ImportViaAPITwoFactorSubmitTAN,
    ImportViaAPITwoFactorRetrievePhotoTAN,
    Upload,

    Test
)

app_name = "importing"

urlpatterns = [
    path('api/', ImportViaAPI.as_view(), name='import-via-api'),
    path('api/running/<str:task_id>/', ImportViaAPIRunning.as_view(), name='import-via-api-running-task'),
    path('api/two_factor/', ImportViaAPITwoFactorSubmitTAN.as_view(), name='import-via-api-two-factor'),
    path('api/two_factor/retrieve_photo_tan/<str:hash_url>/', ImportViaAPITwoFactorRetrievePhotoTAN.as_view(), name='import-via-api-two-factor-retrieve-photo-tan'),

    path('upload/', Upload.as_view(), name='import-upload'),
    path('import/test/', Test.as_view(), name='import-test'),
]