from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppUsersConfig(AppConfig):
    name = 'app_users'
    verbose_name = _('Пользователи')

    def ready(self):
        import NewsPaper.app_users.signals
