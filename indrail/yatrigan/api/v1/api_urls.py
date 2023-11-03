from django.urls import path, include

from indrail.yatrigan.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('station/<station>/stalls', APIv1.ShopListApi.as_view()),
    path('station/<station>/stalls/<shopId>/info', APIv1.ShopInfoApi.as_view()),
    path('trainList', APIv1.TrainListApi.as_view()),
    path('trainSchedule', APIv1.TrainScheduleApi.as_view()),
    #DEV
]
