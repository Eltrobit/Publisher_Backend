from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import File
from .serializers import FileSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class FileViewSet(viewsets.ViewSet):
    """
    API для работы с файлами без аутентификации, используя ID пользователя
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """
        Получить все файлы (только для демонстрации)
        """
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Получить конкретный файл по ID
        """
        file = get_object_or_404(File, id=pk)
        serializer = FileSerializer(file)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Создать новый файл, с передачей ID пользователя в теле запроса
        URL: /api/files/
        """
        try:
            data = request.data
            user_id = data.get('user')
            
            if not user_id:
                return Response(
                    {"error": "ID пользователя (user) обязателен"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Используем стандартную модель пользователя Django
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": f"Пользователь с ID {user_id} не найден"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Удаляем user из данных, так как он передается отдельно при сохранении
            if 'user' in data:
                data = data.copy()
                data.pop('user')
                
            serializer = FileSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'], url_path='user/(?P<user_id>[^/.]+)')
    def user_files(self, request, user_id=None):
        """
        Получить все файлы пользователя по его ID
        URL: /api/files/user/{user_id}/
        """
        try:
            user = get_object_or_404(User, id=user_id)
            files = File.objects.filter(user=user)
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'], url_path='user/(?P<user_id>[^/.]+)/create')
    def create_file(self, request, user_id=None):
        """
        Создать файл для пользователя по его ID
        URL: /api/files/user/{user_id}/create/
        """
        try:
            user = get_object_or_404(User, id=user_id)
            data = request.data
            
            serializer = FileSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['PUT'], url_path='update')
    def update_file(self, request, pk=None):
        """
        Обновить файл по его ID
        URL: /api/files/{file_id}/update/
        """
        try:
            file = get_object_or_404(File, id=pk)
            serializer = FileSerializer(file, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['DELETE'], url_path='delete')
    def delete_file(self, request, pk=None):
        """
        Удалить файл по его ID
        URL: /api/files/{file_id}/delete/
        """
        try:
            file = get_object_or_404(File, id=pk)
            file.delete()
            return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


