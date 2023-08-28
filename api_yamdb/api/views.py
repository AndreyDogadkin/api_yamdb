from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from reviews.models import Title, Category, Genre
from .pagination import TitleCategoryGenrePagination
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .viewsets import ListCreateDeleteViewSet


class TitleViewSet(viewsets.ModelViewSet):
    """CRUD для произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = []
    pagination_class = TitleCategoryGenrePagination
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    search_fields = (
        '^category__slug',
        '^genre__slug',
        '^name',
        'year'
    )
    filterset_fields = (
        'genre',
        'category',
        'name',
        'year'
    )


class CategoryViewSet(ListCreateDeleteViewSet):
    """Создание, представление и удаление категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """Создание, представление и удаление жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
