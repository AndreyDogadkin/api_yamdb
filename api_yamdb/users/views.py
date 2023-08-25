from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from users.serializers import UserSerializerForAuth, UserSerializer, MeSerializer
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.utils.crypto import get_random_string
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'


@api_view(['PATCH', 'GET'])
def me_view(request):
    '''Доступ пользователя к собственной странице'''
    if request.method == 'PATCH':
        obj = get_object_or_404(User, username=request.user.username)
        serializer = MeSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        obj = get_object_or_404(User, username=request.user.username)
        serializer = MeSerializer(obj)
        return Response(serializer.data, status=HTTP_200_OK)


class SignupView(CreateAPIView):
    '''Создание пользователя.
    Сразу после создания на указанный адрес отправляется 
    письмо для подтверждения'''
    
    queryset = User.objects.all()
    serializer_class = UserSerializerForAuth
    permission_classes = [permissions.AllowAny]

    EMAIL_DATA = {
        'subject': 'Confirmation Code',
        'from_email': 'no_reply@example.test',
        'fail_silently': True
    }

    def _send_email(self, recipient:str, confirmation_code: str):
        message = f'There is your confirmation code {confirmation_code}'
        send_mail(recipient_list=[recipient], message=message, **self.EMAIL_DATA)

    def perform_create(self, serializer):
        """Сохраняет код подтверждения в поле юзера
        и отправляет письмо с тем же кодом на указанную в запросе почту"""
        confirmation_code = get_random_string(15)
        serializer.save(confirmation_code=confirmation_code)

        self._send_email(recipient=serializer.data.get('email'),
                         confirmation_code=confirmation_code)
        
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(username=username).count():
            user = User.objects.get(username=username)
            if user.email != email:
                raise ValidationError
            confirmation_code = get_random_string(15)
            user.confirmation_code = confirmation_code
            user.save()
            self._send_email(recipient=email, confirmation_code=confirmation_code)
            return Response({'username': username, 'email': email}, 
                            status=HTTP_200_OK) 
        return super().create(request, *args, **kwargs)


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