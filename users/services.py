import random
import string

from django.conf import settings
from django.core.mail import send_mail


def get_generated_key(digits):
    """Функция генерации токена/пароля"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=digits))


def send_key_mail(token, site, email):
    """Функция отправки токена при регистрации"""
    send_mail(
        subject="Регистрация",
        message=f"Ваш ключ для регистрации: {token}\nФорму ввода можно найти по ссылке: {site}/users/verification",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


def send_password_mail(password, email):
    """Функция отправки пароля при смене пароля"""
    send_mail(
        subject="Смена пароля",
        message=f"Ваш новый пароль: {password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
