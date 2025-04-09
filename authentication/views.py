from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .models import User
from django.db.models import Q

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Автоматически авторизуем пользователя
            login(request, user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        
        # Проверка наличия email и password
        if not email or not password:
            return Response({
                'status': 'error',
                'message': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Поиск пользователя по email или username
        user = User.objects.filter(Q(email=email) | Q(username=email)).first()
        
        if not user:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Аутентификация пользователя
        if not user.check_password(password):
            return Response({
                'status': 'error',
                'message': 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Вход пользователя в систему
        login(request, user)
        
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            'status': 'success',
            'message': 'Logged out successfully'
        })