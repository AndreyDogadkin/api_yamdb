from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from api.pagination import TitleCategoryGenrePagination


class ListCreateDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Базовый ViewSet для создания, представления и удаления."""

    permission_classes = []
    pagination_class = TitleCategoryGenrePagination
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'
