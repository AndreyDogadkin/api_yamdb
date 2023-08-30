from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    ReviewViewSet, CommentViewSet)

router = DefaultRouter()
router.register(prefix='titles', viewset=TitleViewSet)
router.register(prefix='categories', viewset=CategoryViewSet)
router.register(prefix='genres', viewset=GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(router.urls)),
]
