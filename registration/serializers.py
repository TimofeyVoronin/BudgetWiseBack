# registration/serializers.py
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="Ваш email (он будет использоваться как логин)"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        help_text="Пароль минимум 8 символов"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Повторите пароль для подтверждения"
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2')

    def validate(self, attrs):
        # Проверяем, что оба поля есть
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password2": "Пароли не совпадают."})

        # Пропускаем пароль через стандартные валидаторы Django
        try:
            validate_password(password)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        # Убираем password2 перед созданием
        validated_data.pop('password2')

        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        return user
