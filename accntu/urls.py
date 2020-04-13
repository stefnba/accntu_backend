"""accntu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls', namespace='main',)), 
    path('accounts/', include('accounts.urls', namespace='accounts',)),
    path('admin/', admin.site.urls),    
    path('auth/', include('oauth2_provider.urls', namespace='oauth2_provider')), 
    path('budget/', include('budget.urls', namespace='budget',)),
    path('business/', include('business.urls', namespace='business',)),
    path('filtering/', include('filtering.urls', namespace='filtering')), 
    path('import/', include('importing.urls', namespace='importing',)),
    path('transactions/', include('transactions.urls', namespace='transactions',)),
    path('users/', include('users.urls', namespace='users',)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns