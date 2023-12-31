from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Title, Category, Genre, Review
from users.permissions import IsAdminOrHigherOrReadOnly
from .filters import TitleFilterSet
from .pagination import TitleCategoryGenrePagination
from .permissions import IsAuthorOrModerOrAdmin
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, ReviewSerializer,
                          CommentSerializer)
from .viewsets import ListCreateDeleteViewSet, ExcludePutModelViewSet


class TitleViewSet(ExcludePutModelViewSet):
    """CRUD для произведений."""

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
    """Создание, представление и удаление категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrHigherOrReadOnly,)


class GenreViewSet(ListCreateDeleteViewSet):
    """Создание, представление и удаление жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrHigherOrReadOnly,)


class ReviewViewSet(ExcludePutModelViewSet):
    """Отзывы на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        score_count_sum = Review.objects.filter(
            title=title).aggregate(Avg('score'))
        rating = round(score_count_sum.get('score__avg'))
        title.rating = rating
        title.save()


class CommentViewSet(ExcludePutModelViewSet):
    """Комментарии пользователей."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)
