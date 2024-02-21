from django.contrib.auth.models import User

from NewsPaper.app_news.permissions import PUBLISH_NEWS_PERM_CODE_NAME


VERIFIED_USER_GROUP_NAME = 'verified_users_group'
MODERATOR_USER_GROUP_NAME = 'moderator_users_group'
VERIFY_USER_PERM_CODE_NAME = 'can_verify_user'


def user_is_moderator(user: User) -> bool:
    """
    Проверка, является ли пользователь модератором.
    """
    return user.has_perms([f'app_news.{PUBLISH_NEWS_PERM_CODE_NAME}', f'app_users.{VERIFY_USER_PERM_CODE_NAME}'])
