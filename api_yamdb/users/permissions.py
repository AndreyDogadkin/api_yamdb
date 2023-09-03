from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsAuthorOrStaff(IsAuthenticated):

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and (
                request.user.is_superuser
                or request.user.role in ['admin', 'moderator']
            )
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrHigher(IsAuthenticated):

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and (
                request.user.is_superuser
                or request.user.role == 'admin'
            )
        )


class IsAdminOrHigherOrReadOnly(IsAuthenticated):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                super().has_permission(request, view) and (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                )
            )
        )
