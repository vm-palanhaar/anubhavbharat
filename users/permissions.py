from rest_framework.permissions import BasePermission

class IsKyc(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_kyc