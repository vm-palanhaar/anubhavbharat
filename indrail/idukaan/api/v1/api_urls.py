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
            #DEV
        ])),
        #DEV
    ])),
]
