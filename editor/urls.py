from django.urls import path
from .views import *

urlpatterns = [
    path('api/binary', BinaryDocumentViewSet.as_view(), name='BinaryDocument')
]