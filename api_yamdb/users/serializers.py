from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


def validate_username(value):
    if value.lower() == "me":
        raise serializers.ValidationError('username "me" is not allowed')
    return value


class UserSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        return validate_username(value)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'
        optional_fields = ('first_name', 'last_name',
                           'bio', 'role')


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserSerializerForAuth(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=20,
                                              write_only=True,
                                              required=False)

    def validate_username(self, value):
        return validate_username(value)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'confirmation_code')
