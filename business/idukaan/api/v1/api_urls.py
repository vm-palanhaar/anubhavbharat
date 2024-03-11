from django.urls import path, include

from business.idukaan.api.v1 import api_views as APIv1

urlpatterns = [
    #<---PROD--->
    path('org-type-list', APIv1.list_org_types, name = 'get-list-org-types'),
    path('org/add', APIv1.add_org, name = 'post-add-org'),
    path('org/list', APIv1.list_org, name = 'get-list-org'),
    path('org/info', APIv1.org_info, name = 'post-org-info'),
    # org-emp
    path('org/emp/add', APIv1.add_org_emp, name = 'post-add-org-emp'),
    path('org/emp/list', APIv1.list_org_emp, name = 'post-list-org-emp'),
    path('org/emp/update', APIv1.update_org_emp, name = 'patch-org-emp'),
    path('org/emp/delete', APIv1.delete_org_emp, name = 'delete-org-emp'),
    
    #<---DEV--->
    
]
