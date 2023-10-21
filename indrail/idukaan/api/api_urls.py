from django.urls import path, include

urlpatterns = [
    #PROD
    path('v1/', include('indrail.idukaan.api.v1.api_urls')),
    #DEV
]