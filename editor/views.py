from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import File
from .serializers import FileSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the file
        return obj.user == request.user

class FileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing file instances.
    """
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view returns a list of all files
        for the currently authenticated user.
        """
        user = self.request.user
        return File.objects.filter(user=user).order_by('-updated_at')
    
    def create(self, request, *args, **kwargs):
        """
        Create a new file for the current user.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update a file if the current user is the owner.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a file if the current user is the owner.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


