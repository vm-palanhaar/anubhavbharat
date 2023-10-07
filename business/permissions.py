from rest_framework.permissions import BasePermission

class IsOrgTypeView(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.view_orgtype')

class IsOrgAdd(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.add_org')

class IsOrgView(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.view_org')

class IsOrgEmpAdd(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.add_orgemp')
    
class IsOrgEmpView(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.view_orgemp')
    
class IsOrgEmpChange(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.change_orgemp')

class IsOrgEmpDelete(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('business.delete_orgemp')

