from django.urls import path

from users.common.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    #DEV
    path('signup', APIv1.UserSignupApi.as_view()),

]