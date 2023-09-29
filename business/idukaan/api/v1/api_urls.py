from django.urls import path, include

from business.idukaan.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('org/type', APIv1.OrgTypesApi.as_view()),
    path('org', APIv1.OrgApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    #DEV
]