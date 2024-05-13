from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from main_app.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Класс формы регистрации"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Класс профиля пользователя"""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
