from rest_framework import permissions


class IsAuthorOrModerOrAdmin(permissions.BasePermission):
    """Permission for Review and Comment"""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ['admin', 'moderator']
                or (request.user.role == 'user'
                    and request.user == obj.author))

