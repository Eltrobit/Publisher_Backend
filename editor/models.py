from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=255)
    content = models.JSONField()
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_modified']

    def __str__(self):
        return f"{self.name} - {self.user.username}" 