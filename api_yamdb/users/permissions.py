from rest_framework.permissions import IsAuthenticated


class IsSuperUser(IsAuthenticated):

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.is_superuser())


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.role == 'admin')


class IsModerator(IsAuthenticated):

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.role == 'moderator')


class IsAuthor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user