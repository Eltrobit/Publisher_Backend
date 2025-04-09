from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'content', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']