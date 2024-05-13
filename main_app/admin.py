from django.contrib import admin

from main_app.models import Client, Letter, LogMessage, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "created_by",
        "email",
        "name",
        "comment",
    )
    search_fields = (
        "email",
        "name",
    )


@admin.register(Letter)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "letter_title",
        "letter_body",
    )
    search_fields = ("letter_title",)


@admin.register(LogMessage)
class LogMessageAdmin(admin.ModelAdmin):
    list_display = (
        "last_try",
        "sending_status",
        "id_mailing",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "is_active",
        "first_sending_time",
        "period",
        "name",
        "end_datetime",
        "status",
        "created_by",
    )
    search_fields = ("name",)
    filter_fields = (
        "is_active",
        "period",
        "status",
    )
