from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания суперюзера в проекте"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email="admin@sky.pro",
            first_name="Admin",
            last_name="Admin",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password("admin")
        user.save()
