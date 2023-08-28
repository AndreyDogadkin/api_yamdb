from rest_framework import permissions


class IsAuthorOrModerOrAdmin(permissions.BasePermission):
    """Permission for Review and Comment"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user.role in ['admin', 'moderator']
                or (request.user == 'user'
                    and request.user == obj.author)
            )
        return False