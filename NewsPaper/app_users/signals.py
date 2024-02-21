from django.contrib.auth.models import Group
from django.db.models import signals
from django.dispatch import receiver

from NewsPaper.app_users.models import UserProfile
from NewsPaper.app_news.models import News
from NewsPaper.app_users.permissions import VERIFIED_USER_GROUP_NAME


@receiver(signals.pre_save, sender=UserProfile)
def update_user_number_published_news(sender, instance: UserProfile, *args, **kwargs):
    """
    Автоматическое обновление количества опубликованных новостей пользователя, перед сохранением профиля пользователя.
    """
    instance.number_of_published_news = News.objects.filter(author=instance.user).count()
    verified_users_group = Group.objects.get(name=VERIFIED_USER_GROUP_NAME)

    if instance.is_verified:
        instance.user.groups.add(verified_users_group)
    else:
        instance.user.groups.remove(verified_users_group)
