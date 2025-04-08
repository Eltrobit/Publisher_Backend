from django.db import models
from authentication.models import User


class BinaryDocument(models.Model):
    user_id = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    pdf_data = models.BinaryField()  # PDF хранится как бинарные данные

