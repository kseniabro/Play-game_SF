from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppNewsConfig(AppConfig):
    name = 'app_news'
    verbose_name = _('Новости')

    def ready(self):
        import NewsPaper.app_news.signals
