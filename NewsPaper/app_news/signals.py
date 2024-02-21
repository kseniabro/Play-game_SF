from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from uuslug import slugify

from NewsPaper.app_users.models import UserProfile
from NewsPaper.app_news.models import News


@receiver(signals.pre_save, sender=News)
def make_slug(sender, instance: News, *args, **kwargs):
    """
    Сигнал добавления поля slug к новостной сводке и
    обновлением даты публикации, перед сохранением сводки в базу.
    """
    if instance.is_published:
        instance.published_at = timezone.now()
    else:
        instance.published_at = None
    instance.slug = slugify(instance.title)


@receiver(signals.post_save, sender=News)
def update_user_number_published_news_post_news_save(sender, instance: News, created, *args, **kwargs):
    """
    Сигнал на обновление количества созданных новостей пользователем, после создания новостной сводки
    """
    if created:
        profile = UserProfile.objects.get(user=instance.author)
        profile.save()


@receiver(signals.post_delete, sender=News)
def update_user_number_published_news_post_news_del(sender, instance: News, *args, **kwargs):
    """
    Сигнал на обновление количества созданных новостей пользователем, после удаления новостной сводки
    """
    profile = UserProfile.objects.get(user=instance.author)
    profile.save()
