from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Common
    path('user/', include('users.common.api.api_urls')),
    # iDukaan
    path('idukaan/business/', include('business.idukaan.api.api_urls')),
    # Yatrigan
]