from django import template
from django.contrib.auth.models import User

from NewsPaper.app_users.permissions import user_is_moderator

register = template.Library()


@register.filter
def is_moderator(user: User) -> bool:
    """
    Проверка является ли пользователь модератором. Фильтр для шаблонов.
    """
    return user_is_moderator(user)
