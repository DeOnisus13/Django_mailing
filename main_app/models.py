from django.db import models
from django.utils import timezone

from config.settings import NULLABLE
from users.models import User


class Client(models.Model):
    """Модель клиента. Те кто получают рассылки"""

    email = models.EmailField(verbose_name="Email")
    name = models.CharField(max_length=150, verbose_name="ФИО клиента")
    comment = models.TextField(**NULLABLE, verbose_name="Комментарий")
    avatar = models.ImageField(**NULLABLE, upload_to="clients/", verbose_name="Аватар")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Letter(models.Model):
    """Модель письма для рассылки"""

    letter_title = models.CharField(max_length=200, verbose_name="Тема письма")
    letter_body = models.TextField(verbose_name="Тело письма")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.letter_title}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"


class Mailing(models.Model):
    """Модель рассылки"""

    DAILY = "Ежедневно"
    WEEKLY = "Еженедельно"
    MONTHLY = "Ежемесячно"

    PERIOD_CHOICES = {DAILY: "Ежедневно", WEEKLY: "Еженедельно", MONTHLY: "Ежемесячно"}

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = {CREATED: "Создана", STARTED: "Запущена", COMPLETED: "Завершена"}

    name = models.CharField(max_length=150, verbose_name="Имя рассылки")
    client_emails = models.ManyToManyField(Client, verbose_name="Emails")
    letter = models.ForeignKey(Letter, **NULLABLE, on_delete=models.SET, verbose_name="Письмо")
    first_sending_time = models.DateTimeField(**NULLABLE, verbose_name="Время первой рассылки")
    next_sending_time = models.DateTimeField(**NULLABLE, verbose_name="Время следующей рассылки")
    end_datetime = models.DateTimeField(**NULLABLE, verbose_name="Время остановки рассылки")
    period = models.CharField(max_length=150, choices=PERIOD_CHOICES, verbose_name="Период рассылки")
    status = models.CharField(
        default="Создана", max_length=20, **NULLABLE, choices=STATUS_CHOICES, verbose_name="Статус рассылки"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Владелец")

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.client_emails}, {self.letter},"
            f"{self.first_sending_time}, {self.end_datetime},"
            f"{self.period}, {self.status}, {self.is_active}"
        )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

        permissions = [("set_inactive", "Can block mailing")]


class LogMessage(models.Model):
    """Модель лога"""

    SENT = "Успешно"
    FAIL = "Безуспешно"

    LOG_CHOICES = {
        SENT: "Успешно",
        FAIL: "Безуспешно",
    }

    id_mailing = models.ForeignKey(Mailing, **NULLABLE, on_delete=models.CASCADE, verbose_name="Рассылка")
    last_try = models.DateTimeField(**NULLABLE, default=timezone.now, verbose_name="Время последней попытки")
    sending_status = models.CharField(max_length=10, choices=LOG_CHOICES, verbose_name="Статус лога")

    def __str__(self) -> str:
        return f"{self.last_try}, {self.id_mailing}, {self.sending_status}"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
