from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Авторизуем пользователя после регистрации
                login(request, user)
                
                # Возвращаем данные пользователя
                user_data = UserSerializer(user).data
                return Response({
                    'user': user_data,
                    'message': 'Регистрация успешна!'
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return Response({
                    'error': 'Пожалуйста, укажите email и пароль'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Найдем пользователя по email
            try:
                username = User.objects.get(email=email).username
            except User.DoesNotExist:
                return Response({
                    'error': 'Пользователь с таким email не найден'
                }, status=status.HTTP_404_NOT_FOUND)
                
            # Аутентификация по username и password
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Формируем данные пользователя для ответа
                user_data = UserSerializer(user).data
                
                return Response({
                    'user': user_data,
                    'message': 'Вход выполнен успешно!'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Неверный пароль'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Выход выполнен успешно'
        }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    def get(self, request):
        user = request.user
        
        if user.is_authenticated:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({
                'error': 'Пользователь не аутентифицирован'
            }, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = []

    def get(self, request):
        return Response({'success': 'CSRF cookie set'}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class CheckUsersView(APIView):
    permission_classes = []
    
    def get(self, request):
        """
        Отладочное представление для получения списка пользователей
        """
        try:
            users = User.objects.all()
            user_data = []
            
            for user in users:
                user_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                })
            
            return Response({
                'users': user_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)