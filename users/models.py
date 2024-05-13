from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    """Модель Пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="почта")

    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="телефон")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="аватар")
    country = models.CharField(max_length=50, **NULLABLE, verbose_name="страна")
    auth_token = models.CharField(max_length=30, **NULLABLE, verbose_name="ключ")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
