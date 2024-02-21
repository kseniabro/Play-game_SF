from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest

from NewsPaper.app_users import forms
from NewsPaper.app_users import models


def create_new_user(form: forms.RegisterForm):
    """
    Создание нового пользователя, и запись номера телефона в его связный профиль.
    """
    user = form.save()
    telephone = form.cleaned_data.get('telephone')
    models.UserProfile.objects.create(
        user=user,
        telephone=telephone,
    )


def authenticate_user(form: forms.RegisterForm) -> User:
    """
    Аутентификация пользователя.
    """
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)

    return user


def filter_users_queryset_by_username(queryset: QuerySet, request: HttpRequest) -> QuerySet:
    """
    Регистронезависимая фильтрация запроса новостей по полю title.
    """
    username = request.GET.get('username')

    if username:
        queryset = queryset.filter(user__username__icontains=username)

    return queryset


def filter_users_queryset_by_verification(queryset: QuerySet, request: HttpRequest) -> QuerySet:
    """
    Фильтрация запроса новостей по статусу активности новости.
    """
    displayed_news = request.GET.get('displayed_users')

    if displayed_news == 'verified':
        queryset = queryset.filter(is_verified=True)
    elif displayed_news == 'not_verified':
        queryset = queryset.filter(is_verified=False)

    return queryset
