from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания менеджера в проекте"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email="manager@sky.pro",
            is_active=True,
            is_staff=True,
        )
        user.set_password("admin")
        user.save()
