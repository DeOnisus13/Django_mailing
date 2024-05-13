import smtplib

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from main_app.models import Client, LogMessage, Mailing


def start_mailing(class_obj):
    """Функция для отправки рассылок и сохранения результатов в логи"""
    try:
        send_mail(
            subject=class_obj.letter.letter_title,
            message=class_obj.letter.letter_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=list(class_obj.client_emails.all().values_list("email", flat=True)),
            fail_silently=False,
        )
        LogMessage.objects.create(sending_status="Успешно", id_mailing=class_obj)
    except smtplib.SMTPException as e:
        LogMessage.objects.create(sending_status="Безуспешно", id_mailing=class_obj)


def get_cache_mailing_count():
    """Функция для кеширования данных о количестве рассылок"""
    if settings.CACHE_ENABLED:
        key = "mailings_count"
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_mailing_active():
    """Функция для кеширования данных о количестве активных рассылок"""
    if settings.CACHE_ENABLED:
        key = "active_mailings_count"
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_active=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_active=True).count()
    return active_mailings_count


def get_cache_clients_count():
    """Функция для кеширования данных о количестве клиентов"""
    if settings.CACHE_ENABLED:
        key = "clients_count"
        clients_count = cache.get(key)
        if clients_count is None:
            clients_count = Client.objects.distinct().count()
            cache.set(key, clients_count)
    else:
        clients_count = Client.objects.distinct().count()
    return clients_count
