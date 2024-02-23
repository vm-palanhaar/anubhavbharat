from django.urls import path, include

from business.idukaan.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('org-type-list', APIv1.list_org_types, name = 'get-list-org-types'),
    path('org/add', APIv1.add_org, name = 'post-add-org'),
    path('org/list', APIv1.list_org, name = 'get-list-org'),
    path('org/info', APIv1.org_info, name = 'post-org-info'),

    
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
