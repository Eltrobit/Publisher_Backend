from django.shortcuts import render
from rest_framework import viewsets, generics
from editor.models import BinaryDocument
from editor.serializers import BinaryDocumentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class BinaryDocumentViewSet(viewsets.ModelViewSet):
    queryset = BinaryDocument.objects.all()
    serializer_class = BinaryDocumentSerializer


