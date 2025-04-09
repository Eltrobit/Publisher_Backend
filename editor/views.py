from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import File
from .serializers import FileSerializer
from django.utils import timezone

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def save_file(self, request):
        name = request.data.get('name', f'Document {timezone.now().strftime("%Y-%m-%d %H:%M")}')
        content = request.data.get('content', {})
        
        file = File.objects.create(
            user=request.user,
            name=name,
            content=content
        )
        
        return Response({
            'id': file.id,
            'name': file.name,
            'last_modified': file.last_modified,
            'message': 'File saved successfully'
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_file(self, request, pk=None):
        file = self.get_object()
        file.name = request.data.get('name', file.name)
        file.content = request.data.get('content', file.content)
        file.save()
        
        return Response({
            'id': file.id,
            'name': file.name,
            'last_modified': file.last_modified,
            'message': 'File updated successfully'
        })


