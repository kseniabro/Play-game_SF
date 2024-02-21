from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from NewsPaper.app_users import forms, models, views
from NewsPaper.app_users.permissions import MODERATOR_USER_GROUP_NAME
from NewsPaper.project_modules.views import MainView

User = get_user_model()


class LoginUserViewTest(TestCase):
    """
    Тестирование представления LoginUserView
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=cls.username, email=cls.user_email, password=cls.user_password)

    def setUp(self):
        self.auth_url = reverse('app_users:login')

    def test_get_request(self):
        """
        Тестирование GET запроса.
        """
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/login.html')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_post_request_with_username(self):
        """
        Тестирование POST запроса.
        """
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)
        response = self.client.post(self.auth_url,
                                    {'username': self.username, 'password': self.user_password},
                                    follow=True)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('main_view'))
        self.assertEqual(response.resolver_match.func.__name__, MainView.as_view().__name__)

    def test_post_request_with_wrong_data(self):
        """
        Тестирование POST запроса с некорректными данными.
        """
        response = self.client.post(self.auth_url,
                                    {'username': 'wrong_username', 'password': 'wrong_password'},
                                    follow=True)
        exception_message = _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ) % {'username': _('username')}

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/login.html')
        self.assertFormError(response, 'form', None, exception_message)


class LogoutUserViewTest(TestCase):
    """
    Тестирование представления LogoutUserView
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=cls.username, email=cls.user_email, password=cls.user_password)

    def setUp(self):
        self.logout_url = reverse('app_users:logout')

    def test_post_request(self):
        """
        Тестирование POST запроса
        """
        self.client.login(username=self.username, password=self.user_password)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)

        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, reverse('main_view'))
        self.assertEqual(response.resolver_match.func.__name__, MainView.as_view().__name__)
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)

    def test_get_request(self):
        """
        Тестирование GET запроса.
        """
        self.client.login(username=self.username, password=self.user_password)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)

        response = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response, reverse('main_view'))
        self.assertEqual(response.resolver_match.func.__name__, MainView.as_view().__name__)
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)


class RegisterUserViewTest(TestCase):
    """
    Тестирование представления RegisterUserView.
    """

    def setUp(self):
        self.register_url = reverse('app_users:register')
        self.request_data = {
            'username': 'test_username',
            'email': 'test@test.ru',
            'telephone': '123',
            'password1': '123qweQWE',
            'password2': '123qweQWE',
        }

    def test_get_request(self):
        """
        Тестирование GET запроса
        """

        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/register.html')
        self.assertEqual(response.resolver_match.func.__name__, views.RegisterUserView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса.
        """
        response = self.client.post(self.register_url, self.request_data, follow=True)

        user = User.objects.get(pk=1)
        self.assertRedirects(response, reverse('main_view'))
        self.assertEqual(response.resolver_match.func.__name__, MainView.as_view().__name__)
        self.assertEqual(user.username, self.request_data['username'])
        self.assertEqual(user.email, self.request_data['email'])
        self.assertEqual(user.profile.telephone, f'+{self.request_data["telephone"]}')

    def test_post_request_with_strange_telephone_number(self):
        """
        Тестирование POST запроса для проверки корректировки телефонного номера при записи.
        """
        good_phone_number = '1234'
        self.request_data['telephone'] = f'{good_phone_number}bad_phone_number'

        response = self.client.post(self.register_url, self.request_data, follow=True)

        user = User.objects.get(pk=1)
        self.assertRedirects(response, reverse('main_view'))
        self.assertEqual(response.resolver_match.func.__name__, MainView.as_view().__name__)
        self.assertEqual(user.profile.telephone, f'+{good_phone_number}')


class UserProfileViewTest(TestCase):
    """
    Тестирование представления UserProfileView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username, email=cls.user_email, password=cls.user_password)
        models.UserProfile.objects.create(user=user_inst,
                                          telephone=cls.telephone)

    def setUp(self):
        self.profile_url = reverse('app_users:profile')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.profile_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.profile_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.profile_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/profile.html')
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)
        self.assertTrue(isinstance(response.context[forms.UserProfileCityForm.prefix], forms.UserProfileCityForm))
        self.assertTrue(isinstance(response.context[forms.UserProfileTelephoneForm.prefix],
                                   forms.UserProfileTelephoneForm))
        self.assertTrue(isinstance(response.context[forms.UserUsernameForm.prefix], forms.UserUsernameForm))
        self.assertTrue(isinstance(response.context[forms.UserEmailForm.prefix], forms.UserEmailForm))


class UserChangePasswordViewTest(TestCase):
    """
    Тестирование представления UserChangePasswordView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username, email=cls.user_email, password=cls.user_password)
        models.UserProfile.objects.create(user=user_inst,
                                          telephone=cls.telephone)

    def setUp(self):
        self.change_password_url = reverse('app_users:change_password')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.change_password_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.change_password_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.change_password_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/password_change.html')
        self.assertEqual(response.resolver_match.func.__name__, views.UserChangePasswordView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)
        prefix = forms.UserChangePasswordForm.prefix

        response = self.client.post(self.change_password_url,
                                    {f'{prefix}-old_password': self.user_password,
                                     f'{prefix}-new_password1': 'new_pass',
                                     f'{prefix}-new_password2': 'new_pass'},
                                    follow=True)
        url = reverse('app_users:profile')
        self.assertRedirects(response, f"{url}?pass_successfully_changed=True")
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)


class UserProfileTelephoneUpdateViewTest(TestCase):
    """
    Тестирование представления UserProfileTelephoneUpdateView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username, email=cls.user_email, password=cls.user_password)
        cls.profile_inst = models.UserProfile.objects.create(user=user_inst,
                                                             telephone=cls.telephone)

    def setUp(self):
        self.update_telephone_url = reverse('app_users:update_telephone', kwargs={'pk': self.profile_inst.id})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.update_telephone_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.update_telephone_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.update_telephone_url, follow=True)
        self.assertRedirects(response, reverse('app_users:profile'), status_code=301)
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)
        prefix = forms.UserProfileTelephoneForm.prefix
        new_telephone = '+777777'
        self.assertEqual(self.profile_inst.telephone, self.telephone)

        response = self.client.post(self.update_telephone_url,
                                    {f'{prefix}-telephone': new_telephone},
                                    follow=True)

        profile = models.UserProfile.objects.get(id=1)
        self.assertEqual(profile.telephone, new_telephone)
        self.assertRedirects(response, reverse('app_users:profile'))
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)


class UserProfileCityUpdateViewTest(TestCase):
    """
    Тестирование представления UserProfileCityUpdateView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'
    city = 'Город'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username, email=cls.user_email, password=cls.user_password)
        cls.profile_inst = models.UserProfile.objects.create(user=user_inst,
                                                             telephone=cls.telephone,
                                                             city=cls.city)

    def setUp(self):
        self.update_city_url = reverse('app_users:update_city', kwargs={'pk': self.profile_inst.id})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.update_city_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.update_city_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.update_city_url, follow=True)
        self.assertRedirects(response, reverse('app_users:profile'), status_code=301)
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)
        prefix = forms.UserProfileCityForm.prefix
        new_city = 'Новый Город'
        self.assertEqual(self.profile_inst.city, self.city)

        response = self.client.post(self.update_city_url,
                                    {f'{prefix}-city': new_city},
                                    follow=True)

        profile = models.UserProfile.objects.get(id=1)
        self.assertEqual(profile.city, new_city)
        self.assertRedirects(response, reverse('app_users:profile'))
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)


class UserUsernameUpdateViewTest(TestCase):
    """
    Тестирование представления UserUsernameUpdateView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'
    city = 'Город'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User.objects.create_user(username=cls.username,
                                                 email=cls.user_email,
                                                 password=cls.user_password)
        cls.profile_inst = models.UserProfile.objects.create(user=cls.user_inst,
                                                             telephone=cls.telephone,
                                                             city=cls.city)

    def setUp(self):
        self.update_username_url = reverse('app_users:update_username', kwargs={'pk': self.profile_inst.id})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.update_username_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.update_username_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.update_username_url, follow=True)
        self.assertRedirects(response, reverse('app_users:profile'), status_code=301)
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)
        prefix = forms.UserUsernameForm.prefix
        new_username = 'new_username'
        self.assertEqual(self.user_inst.username, self.username)

        response = self.client.post(self.update_username_url,
                                    {f'{prefix}-username': new_username},
                                    follow=True)

        user = User.objects.get(id=1)
        self.assertEqual(user.username, new_username)
        self.assertRedirects(response, reverse('app_users:profile'))
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)


class UserEmailUpdateViewTest(TestCase):
    """
    Тестирование представления UserEmailUpdateView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'
    city = 'Город'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User.objects.create_user(username=cls.username,
                                                 email=cls.user_email,
                                                 password=cls.user_password)
        cls.profile_inst = models.UserProfile.objects.create(user=cls.user_inst,
                                                             telephone=cls.telephone,
                                                             city=cls.city)

    def setUp(self):
        self.update_email_url = reverse('app_users:update_email', kwargs={'pk': self.profile_inst.id})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.update_email_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.update_email_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.update_email_url, follow=True)
        self.assertRedirects(response, reverse('app_users:profile'), status_code=301)
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)
        prefix = forms.UserEmailForm.prefix
        new_email = 'new_email@email.ru'
        self.assertEqual(self.user_inst.email, self.user_email)

        response = self.client.post(self.update_email_url,
                                    {f'{prefix}-email': new_email},
                                    follow=True)

        user = User.objects.get(id=1)
        self.assertEqual(user.email, new_email)
        self.assertRedirects(response, reverse('app_users:profile'))
        self.assertEqual(response.resolver_match.func.__name__, views.UserProfileView.as_view().__name__)


class ModeratorMainViewTest(TestCase):
    """
    Тестирование представления ModeratorMainView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'
    city = 'Город'

    moder_user_name = 'moder_user_name'
    moder_email = 'mader@mail.ru'
    moder_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User.objects.create_user(username=cls.username,
                                                 email=cls.user_email,
                                                 password=cls.user_password)
        cls.profile_inst = models.UserProfile.objects.create(user=cls.user_inst,
                                                             telephone=cls.telephone,
                                                             city=cls.city)

        moder_user_inst = User.objects.create_user(username=cls.moder_user_name,
                                                   email=cls.moder_email,
                                                   password=cls.moder_password)

        moder_group = Group.objects.get(name=MODERATOR_USER_GROUP_NAME)
        moder_group.user_set.add(moder_user_inst)

    def setUp(self):
        self.main_moderator_url = reverse('app_users:main_moderator')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.main_moderator_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.main_moderator_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request_not_moderator(self):
        """
        Тестирование GET запроса не модератором.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.main_moderator_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.ModeratorMainView.as_view().__name__)

    def test_get_request_with_moderator(self):
        """
        Тестирование GET запроса модератором.
        """
        self.client.login(username=self.moder_user_name, password=self.moder_password)

        response = self.client.get(self.main_moderator_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/main_moderation.html')
        self.assertEqual(response.resolver_match.func.__name__, views.ModeratorMainView.as_view().__name__)


class ModerateUsersListViewTest(TestCase):
    """
    Тестирование представления ModerateUsersListView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'
    city = 'Город'

    moder_user_name = 'moder_user_name'
    moder_email = 'mader@mail.ru'
    moder_password = '123qweQWE'

    total_users_count = 20

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        models.UserProfile.objects.create(user=user_inst,
                                          telephone=cls.telephone,
                                          city=cls.city,
                                          is_verified=True)

        for i in range(cls.total_users_count):
            user_inst = User.objects.create_user(username=f"{cls.username} {i}",
                                                 email=cls.user_email,
                                                 password=cls.user_password)
            models.UserProfile.objects.create(user=user_inst,
                                              telephone=f'{cls.telephone}{i}',
                                              city=cls.city)

        moder_user_inst = User.objects.create_user(username=cls.moder_user_name,
                                                   email=cls.moder_email,
                                                   password=cls.moder_password)

        moder_group = Group.objects.get(name=MODERATOR_USER_GROUP_NAME)
        moder_group.user_set.add(moder_user_inst)

    def setUp(self):
        self.users_list_moderation_url = reverse('app_users:users_list_moderation')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.users_list_moderation_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.users_list_moderation_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request_not_moderator(self):
        """
        Тестирование GET запроса не модератором.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.users_list_moderation_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)

    def test_get_request_with_moderator(self):
        """
        Тестирование GET запроса модератором.
        """
        self.client.login(username=self.moder_user_name, password=self.moder_password)

        response = self.client.get(self.users_list_moderation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/users_list_moderation.html')
        self.assertEqual(len(response.context['user_profiles']), 10)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)

    def test_get_request_with_moderator_with_username_filter(self):
        """
        Тестирование GET запроса модератором с фильтрацией по имени пользователя.
        """
        self.client.login(username=self.moder_user_name, password=self.moder_password)

        response = self.client.get(f'{self.users_list_moderation_url}'
                                   f'?username={self.username} {self.total_users_count - 1}',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/users_list_moderation.html')
        self.assertEqual(len(response.context['user_profiles']), 1)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)

    def test_get_request_with_moderator_with_verified_filter(self):
        """
        Тестирование GET запроса модератором с фильтрацией по статусу верификации.
        """
        self.client.login(username=self.moder_user_name, password=self.moder_password)

        response = self.client.get(f'{self.users_list_moderation_url}'
                                   f'?displayed_users=verified',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/users_list_moderation.html')
        self.assertEqual(len(response.context['user_profiles']), 1)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)

    def test_get_request_with_moderator_with_custom_paginate(self):
        """
        Тестирование GET запроса модератором с кастомной пагинацией.
        """
        users_per_page = 15
        self.client.login(username=self.moder_user_name, password=self.moder_password)
        self.client.cookies['users_per_page'] = users_per_page

        response = self.client.get(self.users_list_moderation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/users_list_moderation.html')
        self.assertEqual(len(response.context['user_profiles']), users_per_page)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)

    def test_post_request_with_moderator(self):
        """
        Тестирование POST запроса модератором.
        """
        users_per_page = self.total_users_count + 2
        self.client.login(username=self.moder_user_name, password=self.moder_password)
        self.client.cookies['users_per_page'] = users_per_page

        response_get = self.client.get(self.users_list_moderation_url, follow=True)

        context = {}
        formset_prefix = response_get.context['formset'].management_form.prefix
        for key, value in response_get.context['formset'].management_form.initial.items():
            field_name = f'{formset_prefix}-{key}'
            context[field_name] = value

        for form in response_get.context['formset']:
            prefix = form.prefix
            if form['id'].value():
                context[f'{prefix}-id'] = form['id'].value()
                field_name = f'{prefix}-is_verified'
                context[field_name] = 'on'

        self.assertEqual(len(models.UserProfile.objects.filter(is_verified=True)), 1)

        response_post = self.client.post(self.users_list_moderation_url,
                                         data=context,
                                         follow=True)

        self.assertEqual(len(models.UserProfile.objects.filter(is_verified=True)),
                         self.total_users_count + 1)
        self.assertRedirects(response_post, response_post.wsgi_request.get_full_path())
        self.assertEqual(response_post.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)


class UserModerateViewTest(TestCase):
    """
    Тестирование представления UserModerateView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone = '123'
    city = 'Город'

    moder_user_name = 'moder_user_name'
    moder_email = 'mader@mail.ru'
    moder_password = '123qweQWE'

    total_users_count = 20

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User.objects.create_user(username=cls.username,
                                                 email=cls.user_email,
                                                 password=cls.user_password)
        cls.user_profile_inst = models.UserProfile.objects.create(id=1,
                                                                  user=cls.user_inst,
                                                                  telephone=cls.telephone,
                                                                  city=cls.city)

        moder_user_inst = User.objects.create_user(username=cls.moder_user_name,
                                                   email=cls.moder_email,
                                                   password=cls.moder_password)

        moder_group = Group.objects.get(name=MODERATOR_USER_GROUP_NAME)
        moder_group.user_set.add(moder_user_inst)

    def setUp(self):
        self.user_moderation_url = reverse('app_users:user_moderation', kwargs={'pk': self.user_inst.id})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """
        response = self.client.get(self.user_moderation_url, follow=True)
        url = reverse('app_users:login')
        self.assertRedirects(response, f'{url}?next={self.user_moderation_url}')
        self.assertEqual(response.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса не модератором.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.user_moderation_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.UserModerateView.as_view().__name__)

    def test_get_request_by_moderator(self):
        """
        Тестирование GET запроса модератором.
        """
        self.client.login(username=self.moder_user_name, password=self.moder_password)

        response = self.client.get(self.user_moderation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/user_moderation.html')
        self.assertEqual(response.resolver_match.func.__name__, views.UserModerateView.as_view().__name__)

    def test_post_request_by_moderator(self):
        """
        Тестирование POST запроса модератором.
        """
        self.client.login(username=self.moder_user_name, password=self.moder_password)
        self.assertEqual(self.user_profile_inst.is_verified, False)

        response = self.client.post(self.user_moderation_url,
                                    {'is_verified': True},
                                    follow=True)

        user_profile_inst = models.UserProfile.objects.get(id=1)
        self.assertEqual(user_profile_inst.is_verified, True)
        self.assertRedirects(response, reverse('app_users:users_list_moderation'))
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateUsersListView.as_view().__name__)
