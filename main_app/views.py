from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blogs.models import Blog
from main_app.forms import ClientForm, LetterForm, MailingForm
from main_app.models import Client, Letter, LogMessage, Mailing
from main_app.services import get_cache_clients_count, get_cache_mailing_active, get_cache_mailing_count
from users.models import User


class MainListView(ListView):
    """Контроллер для главной страницы"""

    model = Blog
    template_name = "main_app/homepage.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailings_amount"] = get_cache_mailing_count()
        context["mailings_active"] = get_cache_mailing_active()
        context["clients_amount"] = get_cache_clients_count()
        return context


class ManagerListView(UserPassesTestMixin, ListView):
    """Контроллер для просмотра списка пользователей менеджером с возможностью их деактивации"""

    model = User
    template_name = "main_app/manager.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(is_staff=False)
        return queryset


def toggle_activity_user(request, pk):
    """Функция для изменения статуса пользователя"""
    user_activity = get_object_or_404(User, pk=pk)
    if user_activity.is_active:
        user_activity.is_active = False
    else:
        user_activity.is_active = True
    user_activity.save()
    return redirect(reverse("main_app:manager"))


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для вывода списка клиентов"""

    model = Client
    login_url = reverse_lazy("main_app:homepage")

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset


class ClientDetailView(DetailView):
    """Контроллер для просмотра клиента"""

    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


class ClientCreateView(UserPassesTestMixin, CreateView):
    """Контроллер для создания клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main_app:clients_page")

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name="manager")


class ClientUpdateView(UpdateView):
    """Контроллер для изменения клиента"""

    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("main_app:view_client", args=[self.kwargs.get("pk")])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


class ClientDeleteView(DeleteView):
    """Контроллер для удаления клиента"""

    model = Client
    success_url = reverse_lazy("main_app:clients_page")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


class LetterListView(LoginRequiredMixin, ListView):
    """Контроллер для вывода списка писем"""

    model = Letter
    login_url = reverse_lazy("main_app:homepage")

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset


class LetterDetailView(DetailView):
    """Контроллер для просмотра письма"""

    model = Letter

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


class LetterCreateView(UserPassesTestMixin, CreateView):
    """Контроллер для создания письма"""

    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy("main_app:letters_page")

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name="manager")


class LetterUpdateView(UpdateView):
    """Контроллер для изменения письма"""

    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse("main_app:view_letter", args=[self.kwargs.get("pk")])


class LetterDeleteView(DeleteView):
    """Контроллер для удаления письма"""

    model = Letter
    success_url = reverse_lazy("main_app:letters_page")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


class LogMessageListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка логов"""

    model = LogMessage
    login_url = reverse_lazy("users:login")

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(id_mailing=self.kwargs.get("pk"))
        return queryset


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для вывода списка рассылок"""

    model = Mailing
    login_url = reverse_lazy("main_app:homepage")

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.groups.filter(name="manager") or user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset


class MailingDetailView(DetailView):
    """Контроллер для просмотра рассылки"""

    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user and not user.groups.filter(name="manager"):
            raise Http404("Доступ запрещен")
        return self.object


class MailingCreateView(CreateView):
    """Контроллер для создания рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("main_app:mailing_page")

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name="manager")


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для изменения рассылки"""

    model = Mailing
    form_class = MailingForm
    login_url = reverse_lazy("main_app:homepage")

    def get_success_url(self):
        return reverse("main_app:view_mailing", args=[self.kwargs.get("pk")])

    def test_func(self):
        custom_perms = ("mailing.set_inactive",)
        if self.request.user.groups.filter(name="manager") and self.request.user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


class MailingDeleteView(DeleteView):
    """Контроллер для удаления рассылки"""

    model = Mailing
    success_url = reverse_lazy("main_app:mailing_page")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and self.object.created_by != user:
            raise Http404("Доступ запрещен")
        return self.object


def toggle_activity_mailing(request, pk):
    """Контроллер для изменения статуса рассылки"""
    mailing_status = get_object_or_404(Mailing, pk=pk)
    if mailing_status.is_active:
        mailing_status.is_active = False
    else:
        mailing_status.is_active = True
    mailing_status.save()
    return redirect(reverse("main_app:mailing_page"))
