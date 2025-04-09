from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'binary', BinaryDocumentViewSet, basename='binary')
urlpatterns = [
    path('', include(router.urls))
    #path('binary/', BinaryDocumentViewSet.as_view(), name='BinaryDocument')
]