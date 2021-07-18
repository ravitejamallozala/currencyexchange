from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission


class IsAuthenticatedOrOptions(BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in ["OPTIONS"]
                or request.user
                and is_authenticated(request.user)
        )
