from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from reviews.models import Title, Category, Genre
from .pagination import TitleCategoryGenrePagination
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .viewsets import ListCreateDeleteViewSet


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all().order_by('id')
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

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
