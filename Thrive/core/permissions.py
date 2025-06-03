from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsCompanyManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'MANAGER'

class IsTherapist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'THERAPIST'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'EMPLOYEE'
