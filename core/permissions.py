from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.user_type == 'admin'

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.user_type in ['admin', 'manager']

class IsSalesperson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated