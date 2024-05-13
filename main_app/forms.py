from django import forms
from django.forms import BooleanField, DateTimeInput

from main_app.models import Client, Letter, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("created_by",)


class LetterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Letter
        exclude = ("created_by",)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = (
            "created_by",
            "status",
            "next_sending_time",
        )
        widgets = {
            "first_sending_time": DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "first_sending_time": "Время первой рассылки",
            "end_datetime": "Время остановки рассылки",
        }
