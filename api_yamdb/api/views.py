from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from reviews.models import Title, Category, Genre
from .pagination import TitleCategoryGenrePagination
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .viewsets import ListCreateDeleteViewSet
from .filters import TitleFilterSet


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrHigherOrReadOnly,)
    pagination_class = TitleCategoryGenrePagination
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    search_fields = (
        '^category__slug',
        '^genre__slug',
        '^name',
        'year'
    )
    filterset_class = TitleFilterSet


class CategoryViewSet(ListCreateDeleteViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrHigherOrReadOnly,)


class GenreViewSet(ListCreateDeleteViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrHigherOrReadOnly,)
