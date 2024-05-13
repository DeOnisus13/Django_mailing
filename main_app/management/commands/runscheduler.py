from django.core.management.base import BaseCommand

from main_app.scheduler import start_scheduler


class Command(BaseCommand):
    """Команда запуска рассылок по расписанию"""

    def handle(self, *args, **options):
        start_scheduler()
