# core/permissions.py

from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsCompanyManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'manager'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'

class IsTherapist(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'therapist'
