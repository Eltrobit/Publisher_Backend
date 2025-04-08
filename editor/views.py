from django.shortcuts import render
from rest_framework import viewsets
from editor.models import BinaryDocument
from editor.serializers import BinaryDocumentSerializer

class BinaryDocumentViewSet(viewsets.ModelViewSet):
    queryset = BinaryDocument.objects.all()
    serializer_class = BinaryDocumentSerializer

