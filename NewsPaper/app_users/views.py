from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import FormView, TemplateView, UpdateView

from NewsPaper.app_users import forms
from NewsPaper.app_users import models
from NewsPaper.app_users.forms import UserProfileModerateFormSet
from NewsPaper.app_users import services
from NewsPaper.project_modules.views import CustomPaginateListView, ModeratorMixin, BaseFormsetUpdateView


class LoginUserView(LoginView):
    """
    Вход на сайт под своим пользователем.
    """
    form_class = forms.AuthForm
    template_name = 'app_users/login.html'
    redirect_authenticated_user = True


class LogoutUserView(LogoutView):
    """
    Выход с сайта.
    """
    next_page = reverse_lazy('main_view')


class RegisterUserView(FormView):
    """
    Регистрация нового пользователя.
    """
    form_class = forms.RegisterForm
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('main_view')

    def form_valid(self, form):
        services.create_new_user(form)
        user = services.authenticate_user(form)
        login(self.request, user)
        return super(RegisterUserView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Личная страница пользователя.
    """
    template_name = 'app_users/profile.html'
    login_url = reverse_lazy('app_users:login')
    extra_context = {
        forms.UserProfileCityForm.prefix: forms.UserProfileCityForm(),
        forms.UserProfileTelephoneForm.prefix: forms.UserProfileTelephoneForm(),
        forms.UserUsernameForm.prefix: forms.UserUsernameForm(),
        forms.UserEmailForm.prefix: forms.UserEmailForm(),
    }

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['pass_successfully_changed'] = self.request.GET.get('pass_successfully_changed')

        return context


class BaseUserUpdateView(UserProfileView, UpdateView):
    """
    Базовый класс для обновления данных пользователя.
    """
    success_url = reverse_lazy('app_users:profile')

    def get(self, request, *args, **kwargs):
        return redirect(reverse('app_users:profile'), permanent=True)

    def get_context_data(self, **kwargs):
        context = super(BaseUserUpdateView, self).get_context_data(**kwargs)
        context.update(**kwargs)

        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(**{self.form_class.prefix: form}))


class UserProfileTelephoneUpdateView(BaseUserUpdateView):
    """
    Обновление номера телефона в профиле пользователя.
    """
    form_class = forms.UserProfileTelephoneForm
    model = models.UserProfile


class UserProfileCityUpdateView(BaseUserUpdateView):
    """
    Обновление города в профиле пользователя.
    """
    form_class = forms.UserProfileCityForm
    model = models.UserProfile


class UserUsernameUpdateView(BaseUserUpdateView):
    """
    Обновление имени пользователя.
    """
    form_class = forms.UserUsernameForm
    model = User


class UserEmailUpdateView(BaseUserUpdateView):
    """
    Обновление e-mail пользователя.
    """
    form_class = forms.UserEmailForm
    model = User


class UserChangePasswordView(PasswordChangeView):
    """
    Изменение пароля пользователя.
    """
    form_class = forms.UserChangePasswordForm
    success_url = reverse_lazy('app_users:profile')
    template_name = 'app_users/password_change.html'

    def get_success_url(self):
        url = super(UserChangePasswordView, self).get_success_url()
        return f"{url}?pass_successfully_changed=True"


class ModeratorMainView(ModeratorMixin, TemplateView):
    """
    Главная представление модерации.
    """
    template_name = 'app_users/main_moderation.html'


class ModerateUsersListView(ModeratorMixin, CustomPaginateListView, BaseFormsetUpdateView):
    """
    Представление для вывода всех пользователей для модераторов и возможностью массово менять статус пользователя.
    """
    template_name = 'app_users/users_list_moderation.html'
    queryset = models.UserProfile.objects.select_related('user')
    ordering = 'user'
    context_object_name = 'user_profiles'
    paginate_cookie_name = 'users_per_page'
    formset = UserProfileModerateFormSet

    def get_queryset(self):
        queryset = super(ModerateUsersListView, self).get_queryset()
        queryset = services.filter_users_queryset_by_username(queryset, self.request)
        queryset = services.filter_users_queryset_by_verification(queryset, self.request)

        return queryset


class UserModerateView(ModeratorMixin, generic.UpdateView):
    """
    Модерация пользователя, добавление статуса активности.
    """
    template_name = 'app_users/user_moderation.html'
    form_class = forms.UserProfileVerificationForm
    queryset = models.UserProfile.objects.select_related('user')
    context_object_name = 'user_profile'
    success_url = reverse_lazy('app_users:users_list_moderation')
