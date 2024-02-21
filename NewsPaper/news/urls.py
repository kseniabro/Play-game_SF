from django.contrib import admin
from django.urls import path, include
from NewsPaper.project_modules.views import MainView


urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('admin/', admin.site.urls),
    path('news/', include('app_news.urls')),
    path('users/', include('app_users.urls')),
    path('i18n', include('django.conf.urls.i18n')),
]
