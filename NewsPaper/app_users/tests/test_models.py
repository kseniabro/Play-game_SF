from django.contrib.auth import get_user_model
from django.db.models import SET_NULL, CASCADE
from django.test import TestCase
from django.urls import reverse

from NewsPaper.app_users import models
from NewsPaper.app_news.permissions import PUBLISH_NEWS_PERM_CODE_NAME
from NewsPaper.app_users.models import UserProfile
from NewsPaper.app_users.permissions import VERIFY_USER_PERM_CODE_NAME

User = get_user_model()


class UserProfileTest(TestCase):
    """
    Тестирование модели UserProfile.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        cls.user_profile_inst = UserProfile.objects.create(user=user_inst,
                                                           telephone='123',
                                                           is_verified=True)

    def test_user_verbose_name(self):
        """
        Тестирование verbose_name у поля user.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('user').verbose_name, 'Пользователь')

    def test_user_related_model(self):
        """
        Тестирование related_model у поля user.
        """

        self.assertEquals(self.user_profile_inst._meta.get_field('user').related_model, User)

    def test_user_on_delete(self):
        """
        Тестирование on_delete у поля user.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('user').remote_field.on_delete, CASCADE)

    def test_user_related_name(self):
        """
        Тестирование related_name у поля user.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('user').remote_field.related_name, 'profile')

    def test_telephone_verbose_name(self):
        """
        Тестирование verbose_name у поля telephone.
        """
        field_label = self.user_profile_inst._meta.get_field('telephone').verbose_name
        self.assertEquals(field_label, 'Телефонный номер')

    def test_telephone_max_length(self):
        """
        Тестирование max_length у поля telephone.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('telephone').max_length, 20)

    def test_telephone_unique(self):
        """
        Тестирование unique у поля telephone.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('telephone').unique, True)

    def test_city_verbose_name(self):
        """
        Тестирование verbose_name у поля city.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('city').verbose_name, 'Город проживания')

    def test_city_max_length(self):
        """
        Тестирование max_length у поля city.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('city').max_length, 40)

    def test_city_null(self):
        """
        Тестирование null у поля city.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('city').null, True)

    def test_city_blank(self):
        """
        Тестирование blank у поля city.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('city').blank, True)

    def test_is_verified_verbose_name(self):
        """
        Тестирование verbose_name у поля is_verified.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('is_verified').verbose_name, 'Флаг верификации')

    def test_is_verified_default(self):
        """
        Тестирование max_length у поля is_verified.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('is_verified').default, False)

    def test_number_of_published_news_verbose_name(self):
        """
        Тестирование verbose_name у поля number_of_published_news.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('number_of_published_news').verbose_name,
                          'Количество опубликованных новостей')

    def test_number_of_published_news_default(self):
        """
        Тестирование max_length у поля number_of_published_news.
        """
        self.assertEquals(self.user_profile_inst._meta.get_field('number_of_published_news').default, 0)

    def test_model_verbose_name(self):
        """
        Тестирование verbose_name у модели.
        """
        self.assertEquals(self.user_profile_inst._meta.verbose_name, 'Профиль пользователя')

    def test_model_verbose_name_plural(self):
        """
        Тестирование verbose_name_plural у модели.
        """
        self.assertEquals(self.user_profile_inst._meta.verbose_name_plural, 'Профили пользователей')

    def test_model_permissions(self):
        """
        Тестирование permissions у модели.
        """
        self.assertEquals(self.user_profile_inst._meta.permissions, (
            (VERIFY_USER_PERM_CODE_NAME, "Может верифицировать пользователя"),
        ))

    def test_str_represent_name(self):
        """
        Тестирование текстового представления новости.
        """
        self.assertEquals(self.user_profile_inst.user.username, str(self.user_profile_inst))
