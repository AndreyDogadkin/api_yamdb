from django.urls import path, include
from users.views import SignupView, get_token, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', get_token, name='token_obtain_pair'),
    path('', include(router.urls))
]
