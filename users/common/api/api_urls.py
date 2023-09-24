from django.urls import path, include

urlpatterns = [
    #PROD
    path('v1/', include('users.common.api.v1.api_urls')),
    #DEV
]