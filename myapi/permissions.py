from rest_framework.permissions import BasePermission


class IsEnabled(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.enabled == 1