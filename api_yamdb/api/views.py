from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from reviews.models import Title, Category, Genre, Review, Comment
from .pagination import TitleCategoryGenrePagination
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, CommentSerializer, ReviewSerializer
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы на произвидения."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        reviews = Review.objects.filter(title=title).only('score')
        rating = round(sum(i.score for i in reviews) / reviews.count())
        title.rating = rating
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии пользователей."""

    serializer_class = CommentSerializer
    
    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)
