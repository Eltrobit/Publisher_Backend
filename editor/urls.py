from django.urls import path
from .views import BinaryDocumentViewSet

urlpatterns = [
    path('Binarylist/', BinaryDocumentViewSet.as_view(), name='BinaryDocument'),
]