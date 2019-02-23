from django.urls import path

from .views import (
    Me,
    MeFull,
    Test
)

app_name = "main"


urlpatterns = [

    # My user
    path('me/', Me.as_view(), name='user-me'),
    path('me/full/', MeFull.as_view(), name='user-me'),
    
    # Test
    path('test/', Test.as_view(), name='test'),
]