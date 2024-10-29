from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def unique_username_validator(value):
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError(
            'Логин занят'
        )


def unique_email_validator(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError(
            'Пользователь с таким email уже существует'
        )
