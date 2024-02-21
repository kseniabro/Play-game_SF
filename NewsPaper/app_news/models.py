from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from NewsPaper.app_news.permissions import PUBLISH_NEWS_PERM_CODE_NAME


class News(models.Model):
    """
    Модель Новостных сводок.
    """
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Пользователь'),
                               related_name='news',
                               null=True, )
    title = models.CharField(_('Название'), max_length=100, db_index=True)
    content = models.TextField(_('Содержание'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    published_at = models.DateTimeField(_('Дата публикации'), null=True, blank=True)
    edited_at = models.DateTimeField(_('Дата редактирования'), auto_now=True)
    is_published = models.BooleanField(_('Статус публикации'), db_index=True, default=False)
    slug = models.SlugField('slug-url')

    class Meta:
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')
        ordering = ['-created_at']
        permissions = (
            (PUBLISH_NEWS_PERM_CODE_NAME, _("Может публиковать новости")),
        )

    def get_absolute_url(self):
        return reverse('app_news:news_detail', kwargs={'pk': str(self.id), 'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель комментариев к новостным сводкам
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('Пользователь'),
                             related_name='comments',
                             blank=True,
                             null=True, )

    user_name = models.CharField(_('Имя пользователя'),
                                 max_length=100,
                                 db_index=True,
                                 blank=True,
                                 null=True, )
    text = models.TextField(_('Комментарий'))
    news = models.ForeignKey('News',
                             on_delete=models.CASCADE,
                             verbose_name=_('Новость'),
                             related_name='comments', )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')

    @property
    def get_related_username(self):
        """
        Получение имени пользователя из таблицы User, если такой существует.
        """
        try:
            username = User.objects.get(id=self.user_id).username
        except ObjectDoesNotExist:
            username = None

        return username

    def __str__(self):
        return self.get_related_username or _('{} (аноним)').format(self.user_name)
