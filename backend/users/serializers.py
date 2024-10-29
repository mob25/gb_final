from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxLengthValidator, RegexValidator
from rest_framework import serializers

from .validators import unique_email_validator, unique_username_validator

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[
        MaxLengthValidator(
            254, message='Email не более 254 символа'),
        unique_email_validator])
    username = serializers.CharField(validators=[
        MaxLengthValidator(
            150, message='Логин пользователя не более 150 символов'),
        RegexValidator(regex=r'^[a-z0-9\_]+',
                       message='Недопустимые символы в логине'),
        unique_username_validator])
    first_name = serializers.CharField(required=True, validators=[
        MaxLengthValidator(
            150, message='Имя не более 150 символов'
        )
    ])
    last_name = serializers.CharField(required=True, validators=[
        MaxLengthValidator(
            150, message='Фамилия не более 150 символов'
        )
    ])
    password = serializers.CharField(validators=[
        MaxLengthValidator(
            150, message='Пароль не более 150 символов'
        )
    ])

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserCreateSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class UserReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed')

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return self.context.get('request').user.follower.filter(
            author=obj).exists()
