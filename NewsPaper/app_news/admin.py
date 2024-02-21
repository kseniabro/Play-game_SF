from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from NewsPaper.app_news import models


class CommentInline(admin.TabularInline):
    """
    Inline-форма модели Comment.
    """
    model = models.Comment


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    """
    Административная форма модели News.
    """
    readonly_fields = ['slug']
    list_display = ['title', 'created_at', 'is_published', 'author']
    list_filter = ['is_published', 'author']
    search_fields = ['author__username', 'title']
    inlines = [CommentInline]
    actions = ['activate_news', 'deactivate_news']

    def activate_news(self, request, queryset):
        """
        Сделать выбранные новости активными.
        """
        queryset.update(is_active=True)

    def deactivate_news(self, request, queryset):
        """
        Сделать выбранные новости неактивными.
        """
        queryset.update(is_active=False)

    activate_news.short_description = _('Активировать выбранные новости')
    deactivate_news.short_description = _('Деактивировать выбранные новости')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Административная форма модели Comment.
    """
    list_display = ['user', 'user_name', 'display_text', 'news', 'created_at']
    list_filter = ['user_name']
    actions = ['delete_comment_by_admin']

    def delete_comment_by_admin(self, request, queryset):
        """
        Установить текст комментария "Удален администратором".
        """
        queryset.update(text=_('Комментарий удален администратором'))

    def display_text(self, obj: models.Comment):
        """
        Частично отобразить текст комментария в панели администратора.
        """
        len_to_display = 15
        text = obj.text
        return f'{text[:len_to_display]}...' if len(text) > len_to_display else text

    delete_comment_by_admin.short_description = _('Модерировать выбранные комментарии')
    display_text.short_description = _('Комментарий')
