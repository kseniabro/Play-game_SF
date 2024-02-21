from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from NewsPaper.app_users import models


class UserProfileInline(admin.TabularInline):
    """
    Inline-форма модели UserProfile.
    """
    readonly_fields = ['number_of_published_news']
    model = models.UserProfile
    can_delete = False
    verbose_name = _('Профиль пользователя')
    verbose_name_plural = _('Профили пользователей')


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Административная форма модели UserProfile.
    """
    readonly_fields = ['number_of_published_news', 'user_link']
    list_display = ['user', 'telephone', 'city', 'is_verified', 'number_of_published_news', 'user_link']
    list_filter = ['is_verified']
    actions = ['make_verified', 'make_not_verified']

    def make_verified(self, request, queryset):
        """
        Сделать выбранных пользователей верифицированными
        """
        queryset.update(is_verified=True)

    def make_not_verified(self, request, queryset):
        """
        Убрать у выбранных пользователей верификацию
        """
        queryset.update(is_verified=False)

    def user_link(self, obj: models.UserProfile):
        """
        Добавление ссылки на связную модель пользователя User
        """
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)),
            obj.user.username
        ))

    user_link.short_description = _('Ссылка на связную модель пользователя')
    make_verified.short_description = _('Сделать выбранных пользователей верифицированными')
    make_not_verified.short_description = _('Убрать у выбранных пользователей верификацию')


class CustomUserAdmin(UserAdmin):
    """
    Кастомная административная форма модели User.
    """
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
