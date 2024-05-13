from django.urls import path
from django.views.decorators.cache import cache_page

from main_app.apps import MainAppConfig
from main_app.views import (
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    ClientListView,
    ClientUpdateView,
    LetterCreateView,
    LetterDeleteView,
    LetterDetailView,
    LetterListView,
    LetterUpdateView,
    LogMessageListView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingUpdateView,
    MainListView,
    ManagerListView,
    toggle_activity_mailing,
    toggle_activity_user,
)

app_name = MainAppConfig.name

urlpatterns = [
    path("", MainListView.as_view(), name="homepage"),
    path("manager/", ManagerListView.as_view(), name="manager"),
    path("user_activity/<int:pk>/", toggle_activity_user, name="toggle_activity_user"),

    path("clients/", ClientListView.as_view(), name="clients_page"),
    path("view_client/<int:pk>/", ClientDetailView.as_view(), name="view_client"),
    path("add_client/", ClientCreateView.as_view(), name="add_client"),
    path("update_client/<int:pk>/", ClientUpdateView.as_view(), name="update_client"),
    path("delete_client/<int:pk>/", ClientDeleteView.as_view(), name="delete_client"),

    path("letters/", LetterListView.as_view(), name="letters_page"),
    path("view_letter/<int:pk>/", LetterDetailView.as_view(), name="view_letter"),
    path("add_letter/", LetterCreateView.as_view(), name="add_letter"),
    path("update_letter/<int:pk>/", LetterUpdateView.as_view(), name="update_letter"),
    path("delete_letter/<int:pk>/", LetterDeleteView.as_view(), name="delete_letter"),

    path("view_log/<int:pk>/", cache_page(60)(LogMessageListView.as_view()), name="logs_page"),

    path("mailing/", MailingListView.as_view(), name="mailing_page"),
    path("view_mailing/<int:pk>/", MailingDetailView.as_view(), name="view_mailing"),
    path("add_mailing/", MailingCreateView.as_view(), name="add_mailing"),
    path("update_mailing/<int:pk>/", MailingUpdateView.as_view(), name="update_mailing"),
    path("delete_mailing/<int:pk>/", MailingDeleteView.as_view(), name="delete_mailing"),
    path("mailing_activity/<int:pk>/", toggle_activity_mailing, name="toggle_activity_mailing"),
]
