from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializerForAuth(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=20,
                                              write_only=True,
                                              required=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_user(self, user):
        if user.username == "me":
            raise serializers.ValidationError('username "me" is not allowed')
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'confirmation_code')