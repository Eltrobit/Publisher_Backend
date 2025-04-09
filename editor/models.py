from django.db import models
from django.conf import settings
from django.utils import timezone

class File(models.Model):
    name = models.CharField(max_length=255)
    content = models.JSONField(default=dict)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}" 