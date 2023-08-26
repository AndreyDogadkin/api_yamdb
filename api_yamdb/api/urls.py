from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register(prefix='titles', viewset=TitleViewSet)
router.register(prefix='categories', viewset=CategoryViewSet)
router.register(prefix='genres', viewset=GenreViewSet)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
