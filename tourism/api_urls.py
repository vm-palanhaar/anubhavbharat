from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Common
    path('user/', include('users.api.api_urls')),
    path('ir/', include('indrail.common.api.api_urls')),
    # iDukaan
    path('idukaan/business/', include('business.idukaan.api.api_urls')),
    path('idukaan/ir/', include('indrail.idukaan.api.api_urls')),
    # Yatrigan
    path('yatrigan/ir/', include('indrail.yatrigan.api.api_urls')),
]