from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from main_app.models import Mailing
from main_app.services import start_mailing


def filter_mailing(obj):
    """Функция записывает время следующей отправки в экземпляр класса рассылок с учетом логики,
    и далее вызывает функцию рассылки для подходящих рассылок"""
    now = timezone.localtime(timezone.now())

    if now < obj.end_datetime:
        if not obj.next_sending_time:
            if obj.first_sending_time >= now:
                obj.next_sending_time = obj.first_sending_time
            else:
                if now.time() > obj.first_sending_time.time():
                    obj.next_sending_time = datetime.combine(
                        now.date() + timedelta(days=1), obj.first_sending_time.time()
                    )
                obj.next_sending_time = datetime.combine(now.date(), obj.first_sending_time.time())
            obj.save()

        elif now > obj.next_sending_time:
            start_mailing(obj)
            obj.status = "Запущена"
            if obj.period == "Ежедневно":
                obj.next_sending_time = now + timedelta(days=1)
            elif obj.period == "Еженедельно":
                obj.next_sending_time = now + timedelta(weeks=1)
            elif obj.period == "Ежемесячно":
                obj.next_sending_time = now + timedelta(days=30)
            obj.save()

    elif now > obj.end_datetime:
        obj.status = "Завершена"
        obj.save()


def sending_tasks():
    """Функция фильтрует экземпляры класса рассылок по статусу и передает в другую функцию"""
    mailings = Mailing.objects.filter(status__in=["Создана", "Запущена"])
    if mailings.exists():
        for mailing in mailings:
            if mailing.is_active:
                filter_mailing(mailing)


def start_scheduler():
    """Функция запускает рассылки"""
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    print("Starting scheduler...")
    scheduler.add_job(
        sending_tasks, trigger=CronTrigger(minute="*/1"), id="sending_tasks", max_instances=1, replace_existing=True
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown(wait=False)
