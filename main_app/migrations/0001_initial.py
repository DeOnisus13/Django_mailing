# Generated by Django 5.0.6 on 2024-05-13 04:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("name", models.CharField(max_length=150, verbose_name="ФИО клиента")),
                ("comment", models.TextField(blank=True, null=True, verbose_name="Комментарий")),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="clients/", verbose_name="Аватар")),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Letter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("letter_title", models.CharField(max_length=200, verbose_name="Тема письма")),
                ("letter_body", models.TextField(verbose_name="Тело письма")),
            ],
            options={
                "verbose_name": "Письмо",
                "verbose_name_plural": "Письма",
            },
        ),
        migrations.CreateModel(
            name="LogMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "last_try",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        null=True,
                        verbose_name="Время последней попытки",
                    ),
                ),
                (
                    "sending_status",
                    models.CharField(
                        choices=[("Успешно", "Успешно"), ("Безуспешно", "Безуспешно")],
                        max_length=10,
                        verbose_name="Статус лога",
                    ),
                ),
            ],
            options={
                "verbose_name": "Лог",
                "verbose_name_plural": "Логи",
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Имя рассылки")),
                (
                    "first_sending_time",
                    models.DateTimeField(blank=True, null=True, verbose_name="Время первой рассылки"),
                ),
                (
                    "next_sending_time",
                    models.DateTimeField(blank=True, null=True, verbose_name="Время следующей рассылки"),
                ),
                ("end_datetime", models.DateTimeField(blank=True, null=True, verbose_name="Время остановки рассылки")),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("Ежедневно", "Ежедневно"),
                            ("Еженедельно", "Еженедельно"),
                            ("Ежемесячно", "Ежемесячно"),
                        ],
                        max_length=150,
                        verbose_name="Период рассылки",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("Создана", "Создана"), ("Запущена", "Запущена"), ("Завершена", "Завершена")],
                        default="Создана",
                        max_length=20,
                        null=True,
                        verbose_name="Статус рассылки",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "permissions": [("set_inactive", "Can block mailing")],
            },
        ),
    ]
