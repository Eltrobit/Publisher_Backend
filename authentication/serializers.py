from django.contrib.auth.models import User  # Используем стандартную модель пользователя Django
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Введите корректный email")

        # Проверка на уникальность
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Имя пользователя должно содержать минимум 3 символа")
        
        # Проверка на уникальность
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Пароль должен содержать минимум 6 символов")
        return value

    def create(self, validated_data):
        try:
            # Извлекаем пароль из данных
            password = validated_data.pop('password', None)
            
            # Создаем пользователя без пароля
            user = User.objects.create(**validated_data)
            
            # Устанавливаем пароль правильным способом
            if password:
                user.set_password(password)
                user.save()
            
            return user
        except Exception as e:
            # Логирование ошибки
            print(f"Error creating user: {str(e)}")
            raise serializers.ValidationError(f"Ошибка при создании пользователя: {str(e)}")
            
    def to_representation(self, instance):
        """Преобразуем User в JSON для фронтенда"""
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
        }