from django.urls import path, include
from .views import TitleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(prefix='titles', viewset=TitleViewSet)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]

