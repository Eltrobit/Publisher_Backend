from django.db import models
from django.contrib.auth.models import User  # Используем стандартную модель пользователя Django
from django.utils import timezone

class File(models.Model):
    name = models.CharField(max_length=255)
    content = models.JSONField(default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}" 