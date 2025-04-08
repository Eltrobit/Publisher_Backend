from rest_framework import serializers
from editor.models import BinaryDocument

class BinaruDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryDocument
        fields = "__all__"