from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'content', 'last_modified', 'created_at']
        read_only_fields = ['last_modified', 'created_at']