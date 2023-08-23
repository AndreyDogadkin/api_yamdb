from django.urls import path
from .views import SignupView, get_token


urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('token/', get_token, name='token_obtain_pair'),
]
