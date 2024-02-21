from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from NewsPaper.app_users.permissions import VERIFY_USER_PERM_CODE_NAME


class UserProfile(models.Model):
    """
    Профиль пользователя, дополняет модель User.
    """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                verbose_name=_('Пользователь'),)
    telephone = models.CharField(_('Телефонный номер'),
                                 max_length=20,
                                 unique=True,)
    city = models.CharField(_('Город проживания'),
                            max_length=40,
                            null=True,
                            blank=True,)
    is_verified = models.BooleanField(_('Флаг верификации'), default=False)
    number_of_published_news = models.PositiveIntegerField(_('Количество опубликованных новостей'),
                                                           default=0,)

    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
        permissions = (
            (VERIFY_USER_PERM_CODE_NAME, _("Может верифицировать пользователя")),
        )

    @property
    def get_related_username(self):
        """
        Получение имени пользователя связной модели User.
        """
        return User.objects.get(id=self.user_id).username

    def __str__(self):
        return self.get_related_username
