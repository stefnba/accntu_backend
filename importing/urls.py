from django.urls import path

from .views import (
    ImportViaAPI,
    ImportViaAPIRunning,
    ImportViaAPITwoFactorSubmitTAN,
    ImportViaAPITwoFactorRetrievePhotoTAN,

    Test
)

app_name = "import_transaction"

urlpatterns = [
    path('import/api/', ImportViaAPI.as_view(), name='import-via-api'),
    path('import/api/running/<str:task_id>/', ImportViaAPIRunning.as_view(), name='import-via-api-running-task'),
    path('import/api/two_factor/', ImportViaAPITwoFactorSubmitTAN.as_view(), name='import-via-api-two-factor'),
    path('import/api/two_factor/retrieve_photo_tan/<str:hash_url>/', ImportViaAPITwoFactorRetrievePhotoTAN.as_view(), name='import-via-api-two-factor-retrieve-photo-tan'),

    path('import/test/', Test.as_view(), name='import-test'),
]