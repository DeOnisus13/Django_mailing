from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import ProfileView, RegisterView, RestorePassword, Verification, logout_view

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("verification/", Verification.as_view(), name="verification"),
    path("restore_password/", RestorePassword.as_view(), name="restore_password"),
]
