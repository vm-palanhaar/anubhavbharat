from django.urls import path
from knox import views as knox_views

from users.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('signup', APIv1.UserSignupApi.as_view()),
    path('login', APIv1.UserLoginApi.as_view()),
    path('validate', APIv1.UserLoggedInApi.as_view()),
    path('profile', APIv1.UserProfileApi.as_view()),
    path('logout', knox_views.LogoutView.as_view()),
    path('logoutAll', knox_views.LogoutAllView.as_view()),
    #DEV
]