from django.urls import path, include

from indrail.idukaan.api.v1 import api_views as APIv1

urlpatterns = [
    path('org/', include([
        path('<str:orgId>/', include([
            #PROD
            path('shop', APIv1.ShopApi.as_view({
                'post': 'create',
                'get': 'list',
            })),
            path('shop/<str:shopId>', APIv1.ShopApi.as_view({
                'patch': 'partial_update',
                'get': 'retrieve',
            })),
            path('shop/<str:shopId>/emp', APIv1.ShopEmpApi.as_view({
                'post': 'create',
                'get': 'list',
            })),
            path('shop/<str:shopId>/emp/<str:empId>', APIv1.ShopEmpApi.as_view({
                'patch': 'partial_update',
                'delete': 'destroy',
            })),
            #DEV
        ])),
        #DEV
    ])),
]
