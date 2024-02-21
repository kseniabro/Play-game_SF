from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal
from django.apps.registry import Apps
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from NewsPaper.app_news.permissions import PUBLISH_NEWS_PERM_CODE_NAME
from NewsPaper.app_users.permissions import VERIFIED_USER_GROUP_NAME, MODERATOR_USER_GROUP_NAME, VERIFY_USER_PERM_CODE_NAME


def create_groups(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    """
    Создание групп пользователей (Верифицированные и модераторы) и раздача им необходимых прав доступа.
    """
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, db_alias)

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    moderator_user_permissions = list(Permission.objects.filter(content_type__app_label='app_news',
                                                                content_type__model='news'))
    verified_user_permissions = list(filter(lambda perm: perm.codename != PUBLISH_NEWS_PERM_CODE_NAME,
                                            moderator_user_permissions))

    permission_can_verify_user = list(Permission.objects.filter(codename=VERIFY_USER_PERM_CODE_NAME))
    moderator_user_permissions.extend(permission_can_verify_user)

    moderator_users_group = Group.objects.get_or_create(name=MODERATOR_USER_GROUP_NAME)[0]
    moderator_users_group.permissions.set(moderator_user_permissions)

    verified_users_group = Group.objects.get_or_create(name=VERIFIED_USER_GROUP_NAME)[0]
    verified_users_group.permissions.set(verified_user_permissions)


def delete_groups(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    """
    Удаление созданных групп пользователей (Верифицированные и модераторы).
    """
    Group = apps.get_model('auth', 'Group')

    created_groups = Group.objects.filter(name__in=[VERIFIED_USER_GROUP_NAME, MODERATOR_USER_GROUP_NAME])
    created_groups.delete()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('app_users', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app_news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]
