from typing import Any
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from users.serializers import UserSerializerForAuth
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.utils.crypto import get_random_string


User = get_user_model()


class SignupView(CreateAPIView):
    '''Создание пользователя.
    Сразу после создания на указанный адрес отправляется 
    письмо для подтверждения'''

    EMAIL_DATA = {}
    EMAIL_DATA['subject'] = 'Confirmation Code'
    EMAIL_DATA['from_email'] = 'no_reply@example.test'
    EMAIL_DATA['fail_silently'] = False
    
    queryset = User.objects.all()
    serializer_class = UserSerializerForAuth
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Сохраняет код подтверждения в поле юзера
        и отправляет письмо с тем же кодом на указанную в запросе почту"""
        confirmation_code = get_random_string(15)
        serializer.save(confirmation_code=confirmation_code)

        send_mail(recipient_list=[serializer.data.get('email')],
                  message=f'There is your confirmation code {confirmation_code}',
                  **self.EMAIL_DATA)


@api_view(['POST']) 
@permission_classes([AllowAny])
def get_token(request):
    """Получение jwt-токена. Верификация пользователя по 
    коду подтверждения"""

    user = get_object_or_404(User, username=request.data['username'])

    if user.confirmation_code == request.data.get('confirmation_code'):
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status=HTTP_200_OK) 
    
    return Response({'error': 'confirmation_code is not valid'},
                    status=HTTP_400_BAD_REQUEST) 