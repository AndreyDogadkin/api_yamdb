from rest_framework import mixins, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.pagination import TitleCategoryGenrePagination


class ListCreateDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Базовый ViewSet для создания, представления и удаления."""

    pagination_class = TitleCategoryGenrePagination
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'


class ExcludePutModelViewSet(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
