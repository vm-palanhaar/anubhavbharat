from django.urls import path, include

from business.idukaan.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('org/type', APIv1.OrgTypesApi.as_view()),
    path('org', APIv1.OrgApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('org/<str:orgId>', APIv1.OrgApi.as_view({
        'get': 'retrieve',
    })),
    #DEV
    path('org/<str:orgId>/emp', APIv1.OrgEmpApi.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('org/<str:orgId>/emp/<str:orgEmpId>', APIv1.OrgEmpApi.as_view({
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
]
