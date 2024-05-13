from datetime import date

from django.db import models

from config.settings import NULLABLE


class Blog(models.Model):
    """Модель Блога"""

    header = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(**NULLABLE, verbose_name="Содержимое")
    preview = models.ImageField(upload_to="blogs/", **NULLABLE, verbose_name="Превью")
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")
    created_at = models.DateField(default=date.today, verbose_name="Дата публикации")

    def __str__(self):
        return f"{self.header}, {self.description}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
