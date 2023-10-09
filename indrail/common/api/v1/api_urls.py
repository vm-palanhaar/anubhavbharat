from django.urls import path, include

from indrail.common.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('stations', APIv1.RailStationListApi.as_view()),
    #DEV
]
