import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Publisher_Backend.settings")
django.setup()

from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User

# Создаем тестового пользователя или берем существующего
user = User.objects.first()
if not user:
    print("Нет пользователей в базе данных")
    exit(1)

print(f"Тестирование JWT для пользователя: {user.email} (ID: {user.id})")

# Создаем токены
refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)

print(f"Access Token: {access_token}")
print(f"Refresh Token: {str(refresh)}")

# Проверяем, что в токене есть правильные данные
print("\nПроверка токена:")
token_data = refresh.access_token.payload
print(f"Token Payload: {token_data}")

if 'user_id' in token_data:
    print(f"USER_ID в токене: {token_data['user_id']}")
else:
    print("ОШИБКА: В токене нет поля user_id!")
    print("Проверьте настройки SIMPLE_JWT в settings.py") 