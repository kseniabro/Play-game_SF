import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from NewsPaper.app_news import models, views
from NewsPaper.app_users.models import UserProfile
from NewsPaper.app_users.permissions import MODERATOR_USER_GROUP_NAME
from NewsPaper.app_users.views import LoginUserView

User = get_user_model()


class NewsListViewTest(TestCase):
    """
    Тестирование представления NewsListView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    single_username = 'test_single_username'
    single_user_email = 'single_test@test.ru'
    single_user_password = '123qweQWE'

    total_news = 100
    base_published_title = 'Опубликованное название'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)

        single_user_inst = User.objects.create_user(username=cls.single_username,
                                                    email=cls.single_user_email,
                                                    password=cls.single_user_password)

        news_list = []

        base_published_content = 'Содержание Опубликованной новости'
        base_not_published_title = 'Не опубликованное название'
        base_not_published_content = 'Содержание неопубликованной новости'

        for i in range(cls.total_news):
            published_title = f'{cls.base_published_title} {i}'
            published_content = f'{base_published_content} {i}' * 100
            news_list.append(models.News(author=user_inst,
                                         title=published_title,
                                         content=published_content,
                                         is_published=True,
                                         published_at=timezone.now(),
                                         slug=slugify(published_title)))

            not_published_title = f'{base_not_published_title} {i}'
            not_published_content = f'{base_not_published_content} {i}' * 100
            news_list.append(models.News(author=user_inst,
                                         title=not_published_title,
                                         content=not_published_content,
                                         is_published=False,
                                         slug=slugify(not_published_title)))

        news_list.append(models.News(author=single_user_inst,
                                     title='single_user_inst title',
                                     content='single_user_inst content',
                                     is_published=True,
                                     published_at=timezone.now(),
                                     slug=slugify('single_user_inst title')))

        models.News.objects.bulk_create(news_list)

    def setUp(self):
        self.news_list_url = reverse('app_news:news_list')

    def test_get_request(self):
        """
        Тестирование GET запроса.
        """
        response = self.client.get(self.news_list_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), 10)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_with_custom_paginate(self):
        """
        Тестирование GET запроса c кастомной пагинацией.
        """
        news_per_page = 20

        self.client.cookies['news_per_page'] = news_per_page
        response = self.client.get(self.news_list_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), news_per_page)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_only_published_news(self):
        """
        Тестирование GET запроса c кастомной пагинацией.
        """
        news_per_page = 200

        self.client.cookies['news_per_page'] = news_per_page
        response = self.client.get(self.news_list_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), self.total_news + 1)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_with_filter_by_news_date_end(self):
        """
        Тестирование GET запроса c фильтрацией по дате news_date_end
        """
        news_date_end = datetime.datetime.now() - datetime.timedelta(days=1)

        url = f'{self.news_list_url}' \
              f'?news_date_end={news_date_end.year}-{news_date_end.month}-{news_date_end.day}'

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), 0)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_with_filter_by_news_date_begin(self):
        """
        Тестирование GET запроса c фильтрацией по дате news_date_begin
        """
        news_date_begin = datetime.datetime.now() + datetime.timedelta(days=1)

        url = f'{self.news_list_url}' \
              f'?news_date_begin={news_date_begin.year}-{news_date_begin.month}-{news_date_begin.day}'

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), 0)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_with_filter_by_news_date_with_wrong_data(self):
        """
        Тестирование GET запроса c фильтрацией по дате c некорректными данными даты
        """
        wrong_data = 'wrong_data'

        url = f'{self.news_list_url}' \
              f'?news_date_begin={wrong_data}'

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_with_filter_by_news_title(self):
        """
        Тестирование GET запроса c фильтрацией по названию новости
        """
        news_title = f'{self.base_published_title} 99'

        url = f'{self.news_list_url}?news_title={news_title}'

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), 1)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)

    def test_get_request_with_filter_by_news_author(self):
        """
        Тестирование GET запроса c фильтрацией по имени автора
        """

        url = f'{self.news_list_url}?news_author={self.single_username}'

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        self.assertEqual(len(response.context['news']), 1)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsListView.as_view().__name__)


class ModerateNewsListViewTest(TestCase):
    """
    Тестирование представления ModerateNewsListView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    total_published_news = 100
    total_not_published_news = 50
    base_published_title = 'Опубликованное название'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        UserProfile.objects.create(user=user_inst,
                                   telephone='123',
                                   is_verified=True)

        moder_group = Group.objects.get(name=MODERATOR_USER_GROUP_NAME)
        moder_group.user_set.add(user_inst)

        news_list = []

        base_published_content = 'Содержание Опубликованной новости'
        base_not_published_title = 'Не опубликованное название'
        base_not_published_content = 'Содержание неопубликованной новости'

        for i in range(cls.total_published_news):
            published_title = f'{cls.base_published_title} {i}'
            published_content = f'{base_published_content} {i}' * 100
            news_list.append(models.News(author=user_inst,
                                         title=published_title,
                                         content=published_content,
                                         is_published=True,
                                         published_at=timezone.now(),
                                         slug=slugify(published_title)))

        for i in range(cls.total_not_published_news):
            not_published_title = f'{base_not_published_title} {i}'
            not_published_content = f'{base_not_published_content} {i}' * 100
            news_list.append(models.News(author=user_inst,
                                         title=not_published_title,
                                         content=not_published_content,
                                         is_published=False,
                                         slug=slugify(not_published_title)))

        models.News.objects.bulk_create(news_list)

    def setUp(self):
        self.news_list_moderation_url = reverse('app_news:news_list_moderation')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированного пользователя.
        """
        response = self.client.get(self.news_list_moderation_url, follow=True)
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.news_list_moderation_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_by_moderator(self):
        """
        Тестирование GET запроса модератором.
        """
        self.client.cookies['news_per_page'] = self.total_published_news + self.total_not_published_news
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.news_list_moderation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list_moderation.html')
        self.assertEqual(len(response.context['news']), self.total_published_news + self.total_not_published_news)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateNewsListView.as_view().__name__)

    def test_get_request_by_moderator_only_active_news(self):
        """
        Тестирование GET запроса модератором только активных новостей.
        """
        self.client.cookies['news_per_page'] = self.total_published_news + 1
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(f'{self.news_list_moderation_url}?displayed_news=active', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list_moderation.html')
        self.assertEqual(len(response.context['news']), self.total_published_news)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateNewsListView.as_view().__name__)

    def test_get_request_by_moderator_only_not_active_news(self):
        """
        Тестирование GET запроса модератором только не активных новостей.
        """
        self.client.cookies['news_per_page'] = self.total_not_published_news + 1
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(f'{self.news_list_moderation_url}?displayed_news=not_active', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list_moderation.html')
        self.assertEqual(len(response.context['news']), self.total_not_published_news)
        self.assertEqual(response.resolver_match.func.__name__, views.ModerateNewsListView.as_view().__name__)

    def test_post_request_by_moderator(self):
        """
        Тестирование POST запроса модератором.
        """
        self.client.cookies['news_per_page'] = self.total_not_published_news
        self.client.login(username=self.username, password=self.user_password)

        response_get = self.client.get(f'{self.news_list_moderation_url}?displayed_news=not_active', follow=True)

        context = {}
        formset_prefix = response_get.context['formset'].management_form.prefix
        for key, value in response_get.context['formset'].management_form.initial.items():
            field_name = f'{formset_prefix}-{key}'
            context[field_name] = value

        for form in response_get.context['formset']:
            prefix = form.prefix
            if form['id'].value():
                context[f'{prefix}-id'] = form['id'].value()
                field_name = f'{prefix}-is_published'
                context[field_name] = 'on'

        self.assertEqual(len(models.News.objects.filter(is_published=True)), self.total_published_news)
        response_post = self.client.post(f'{self.news_list_moderation_url}?displayed_news=not_active',
                                         data=context,
                                         follow=True)

        self.assertEqual(len(models.News.objects.filter(is_published=True)),
                         self.total_published_news + self.total_not_published_news)
        self.assertRedirects(response_post, response_post.wsgi_request.get_full_path())
        self.assertEqual(response_post.resolver_match.func.__name__, views.ModerateNewsListView.as_view().__name__)


class PersonalNewsListViewTest(TestCase):
    """
    Тестирование представления PersonalNewsListView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    total_user_news = 100
    base_published_title = 'Опубликованное название'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        UserProfile.objects.create(user=user_inst,
                                   telephone='123',
                                   is_verified=True)

        news_list = []

        base_published_content = 'Содержание Опубликованной новости'
        base_not_published_title = 'Не опубликованное название'
        base_not_published_content = 'Содержание неопубликованной новости'

        for i in range(cls.total_user_news):
            published_title = f'{cls.base_published_title} {i}'
            published_content = f'{base_published_content} {i}' * 100
            news_list.append(models.News(author=user_inst,
                                         title=published_title,
                                         content=published_content,
                                         is_published=True,
                                         published_at=timezone.now(),
                                         slug=slugify(published_title)))

        for i in range(cls.total_user_news):
            not_published_title = f'{base_not_published_title} {i}'
            not_published_content = f'{base_not_published_content} {i}' * 100
            news_list.append(models.News(title=not_published_title,
                                         content=not_published_content,
                                         is_published=False,
                                         slug=slugify(not_published_title)))

        models.News.objects.bulk_create(news_list)

    def setUp(self):
        self.personal_news_list_url = reverse('app_news:personal_news_list')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированного пользователя.
        """
        response = self.client.get(self.personal_news_list_url, follow=True)
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.personal_news_list_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_with_auth_user(self):
        """
        Тестирование GET запроса аутентифицированным пользователем, владельцем новостей.
        """
        self.client.cookies['news_per_page'] = self.total_user_news + 1
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.personal_news_list_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/personal_news_list.html')
        self.assertEqual(len(response.context['news']), self.total_user_news)
        self.assertEqual(response.resolver_match.func.__name__, views.PersonalNewsListView.as_view().__name__)


class NewsDetailCommentCreateViewTest(TestCase):
    """
    Тестирование представления NewsDetailCommentCreateView.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    moder_username = 'moder_test_username'
    moder_user_email = 'moder_test@test.ru'
    moder_user_password = '123qweQWE'

    published_title = 'Опубликованное название'
    published_content = 'Содержание Опубликованной новости' * 100

    not_published_title = 'Не опубликованное название'
    not_published_content = 'Содержание неопубликованной новости'

    comments_length = 10

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        UserProfile.objects.create(user=user_inst,
                                   telephone='123',
                                   is_verified=True)

        moder_int = User.objects.create_user(username=cls.moder_username,
                                             email=cls.moder_user_email,
                                             password=cls.moder_user_password)

        my_group = Group.objects.get(name=MODERATOR_USER_GROUP_NAME)
        my_group.user_set.add(moder_int)

        cls.published_news = models.News.objects.create(author=user_inst,
                                                        title=cls.published_title,
                                                        content=cls.published_content,
                                                        is_published=True,
                                                        published_at=timezone.now(),
                                                        slug=slugify(cls.published_title))

        comments_list = []
        for i in range(cls.comments_length):
            comments_list.append(models.Comment(text='comment_text',
                                                news=cls.published_news))

        models.Comment.objects.bulk_create(comments_list)

        cls.not_published_news = models.News.objects.create(author=user_inst,
                                                            title=cls.not_published_title,
                                                            content=cls.not_published_content,
                                                            is_published=False,
                                                            published_at=timezone.now(),
                                                            slug=slugify(cls.published_title))

    def setUp(self):
        self.published_news_url = reverse('app_news:news_detail', kwargs={'pk': self.published_news.id,
                                                                          'slug': self.published_news.slug})
        self.not_published_news_url = reverse('app_news:news_detail', kwargs={'pk': self.not_published_news.id,
                                                                              'slug': self.not_published_news.slug})

    def test_get_request_to_published_news(self):
        """
        Тестирование GET запроса к опубликованной новости.
        """
        response = self.client.get(self.published_news_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_detail.html')
        self.assertEqual(len(response.context['news'].all_comments), self.comments_length)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDetailCommentCreateView.as_view().__name__)

    def test_get_request_not_auth_user_to_not_published_news(self):
        """
        Тестирование GET запроса не аутентифицированного пользователя к неопубликованной новости.
        """
        response = self.client.get(self.not_published_news_url, follow=True)
        next_url = reverse('app_news:news_update', kwargs={'pk': self.not_published_news.id,
                                                           'slug': self.not_published_news.slug})
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={next_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_by_news_owner_to_not_published_news(self):
        """
        Тестирование GET запроса владельцем новости к неопубликованной новости.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.get(self.not_published_news_url, follow=True)
        next_url = reverse('app_news:news_update', kwargs={'pk': self.not_published_news.id,
                                                           'slug': self.not_published_news.slug})
        self.assertRedirects(response, next_url)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsUpdateView.as_view().__name__)

    def test_get_request_by_moderator_to_not_published_news(self):
        """
        Тестирование GET запроса модератором к неопубликованной новости.
        """
        self.client.login(username=self.moder_username, password=self.moder_user_password)

        response = self.client.get(self.not_published_news_url, follow=True)
        next_url = reverse('app_news:news_moderation', kwargs={'pk': self.not_published_news.id,
                                                               'slug': self.not_published_news.slug})
        self.assertRedirects(response, next_url)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsModerateView.as_view().__name__)

    def test_post_request_to_published_news_not_auth_user(self):
        """
        Тестирование POST запроса к опубликованной новости.
        """
        response = self.client.post(self.published_news_url,
                                    {'text': 'comment_text',
                                     'user_name': 'username'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_detail.html')
        self.assertEqual(len(response.context['news'].all_comments), self.comments_length + 1)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDetailCommentCreateView.as_view().__name__)

    def test_post_request_to_published_news_not_auth_user_with_wrong_text(self):
        """
        Тестирование POST запроса к опубликованной новости с неправильным полем text.
        """
        response = self.client.post(self.published_news_url,
                                    {'text': '',
                                     'user_name': 'username'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_detail.html')
        self.assertFormError(response, 'form', 'text', _('This field is required.'))
        self.assertEqual(len(response.context['news'].all_comments), self.comments_length)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDetailCommentCreateView.as_view().__name__)

    def test_post_request_to_published_news_not_auth_user_with_wrong_user_name(self):
        """
        Тестирование POST запроса к опубликованной новости с неправильным полем user_name.
        """
        response = self.client.post(self.published_news_url,
                                    {'text': 'comment text'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_detail.html')
        self.assertFormError(response, 'form', 'user_name', 'Необходимо ввести имя пользователя')
        self.assertEqual(len(response.context['news'].all_comments), self.comments_length)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDetailCommentCreateView.as_view().__name__)

    def test_post_request_to_published_news_by_auth_user(self):
        """
        Тестирование POST запроса к опубликованной новости аутентифицированным пользователем.
        """
        self.client.login(username=self.username, password=self.user_password)

        response = self.client.post(self.published_news_url,
                                    {'text': 'comment_text'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_detail.html')
        self.assertEqual(len(response.context['news'].all_comments), self.comments_length + 1)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDetailCommentCreateView.as_view().__name__)


class NewsCreateViewTest(TestCase):
    """
    Тестирование представления NewsCreateView.
    """
    verified_username = 'test_username'
    verified_user_email = 'test@test.ru'
    verified_user_password = '123qweQWE'

    not_verified_username = 'not_verified__test_username'
    not_verified_user_email = 'not_virified__test@test.ru'
    not_verified_user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        verified_user_inst = User.objects.create_user(username=cls.verified_username,
                                                      email=cls.verified_user_email,
                                                      password=cls.verified_user_password)
        UserProfile.objects.create(user=verified_user_inst,
                                   telephone='123',
                                   is_verified=True)

        not_verified_user_inst = User.objects.create_user(username=cls.not_verified_username,
                                                          email=cls.not_verified_user_email,
                                                          password=cls.not_verified_user_password)
        UserProfile.objects.create(user=not_verified_user_inst,
                                   telephone='1234', )

    def setUp(self):
        self.published_news_url = reverse('app_news:news_create')

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """

        response = self.client.get(self.published_news_url, follow=True)
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.published_news_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_not_verified_user(self):
        """
        Тестирование GET запроса не верифицированным пользователем.
        """
        self.client.login(username=self.not_verified_username, password=self.not_verified_user_password)

        response = self.client.get(self.published_news_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsCreateView.as_view().__name__)

    def test_get_request_verified_user(self):
        """
        Тестирование GET запроса не верифицированным пользователем.
        """
        self.client.login(username=self.verified_username, password=self.verified_user_password)

        response = self.client.get(self.published_news_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_create.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsCreateView.as_view().__name__)

    def test_post_request_verified_user(self):
        """
        Тестирование POST запроса не верифицированным пользователем.
        """
        self.client.login(username=self.verified_username, password=self.verified_user_password)

        response = self.client.post(self.published_news_url,
                                    {'title': 'title',
                                     'content': 'content'},
                                    follow=True)
        news_inst = models.News.objects.all()[0]
        redirect_url = reverse('app_news:news_update', kwargs={'pk': news_inst.id, 'slug': news_inst.slug})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsUpdateView.as_view().__name__)

    def test_post_request_verified_user_with_wrong_data(self):
        """
        Тестирование POST запроса не верифицированным пользователем с некорректными данными.
        """
        self.client.login(username=self.verified_username, password=self.verified_user_password)

        response = self.client.post(self.published_news_url,
                                    {'title': '',
                                     'content': ''},
                                    follow=True)
        self.assertFormError(response, 'form', 'title', _('This field is required.'))
        self.assertFormError(response, 'form', 'content', _('This field is required.'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_create.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsCreateView.as_view().__name__)


class NewsDeleteViewTest(TestCase):
    """
    Тестирование представления NewsDeleteView.
    """
    news_owner_username = 'test_username'
    news_owner_user_email = 'test@test.ru'
    news_owner_user_password = '123qweQWE'

    other_username = 'other_test_username'
    other_user_email = 'other_test@test.ru'
    other_user_password = '123qweQWE'

    news_title = 'Опубликованное название'
    news_content = 'Содержание Опубликованной новости' * 100

    @classmethod
    def setUpTestData(cls):
        verified_user_inst = User.objects.create_user(username=cls.news_owner_username,
                                                      email=cls.news_owner_user_email,
                                                      password=cls.news_owner_user_password)
        UserProfile.objects.create(user=verified_user_inst,
                                   telephone='123',
                                   is_verified=True)
        cls.published_news = models.News.objects.create(author=verified_user_inst,
                                                        title=cls.news_title,
                                                        content=cls.news_content,
                                                        is_published=True,
                                                        published_at=timezone.now(),
                                                        slug=slugify(cls.news_title))

        other_user_inst = User.objects.create_user(username=cls.other_username,
                                                   email=cls.other_user_email,
                                                   password=cls.other_user_password)
        UserProfile.objects.create(user=other_user_inst,
                                   telephone='1234',
                                   is_verified=True)

    def setUp(self):
        self.delete_news_url = reverse('app_news:news_delete', kwargs={'pk': self.published_news.id,
                                                                       'slug': self.published_news.slug})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """

        response = self.client.get(self.delete_news_url, follow=True)
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.delete_news_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_other_user(self):
        """
        Тестирование GET запроса сторонним пользователем.
        """
        self.client.login(username=self.other_username, password=self.other_user_password)

        response = self.client.get(self.delete_news_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDeleteView.as_view().__name__)

    def test_get_request_news_owner(self):
        """
        Тестирование GET запроса владельцем новости.
        """
        self.client.login(username=self.news_owner_username, password=self.news_owner_user_password)

        response = self.client.get(self.delete_news_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_update.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDeleteView.as_view().__name__)

    def test_post_request_news_owner(self):
        """
        Тестирование POST запроса владельцем новости.
        """
        self.client.login(username=self.news_owner_username, password=self.news_owner_user_password)
        self.assertEqual(len(models.News.objects.all()), 1)

        response = self.client.post(self.delete_news_url, follow=True)
        self.assertEqual(len(models.News.objects.all()), 0)
        url = reverse('app_news:personal_news_list')
        self.assertRedirects(response,
                             f"{url}?news_successfully_delete=True&deleted_news_title={self.published_news.title}")
        self.assertEqual(response.resolver_match.func.__name__, views.PersonalNewsListView.as_view().__name__)


class NewsUpdateViewTest(TestCase):
    """
    Тестирование представления NewsUpdateView.
    """
    news_owner_username = 'test_username'
    news_owner_user_email = 'test@test.ru'
    news_owner_user_password = '123qweQWE'

    other_username = 'other_test_username'
    other_user_email = 'other_test@test.ru'
    other_user_password = '123qweQWE'

    news_title = 'Опубликованное название'
    news_content = 'Содержание Опубликованной новости' * 100

    @classmethod
    def setUpTestData(cls):
        verified_user_inst = User.objects.create_user(username=cls.news_owner_username,
                                                      email=cls.news_owner_user_email,
                                                      password=cls.news_owner_user_password)
        UserProfile.objects.create(user=verified_user_inst,
                                   telephone='123',
                                   is_verified=True)
        cls.published_news = models.News.objects.create(author=verified_user_inst,
                                                        title=cls.news_title,
                                                        content=cls.news_content,
                                                        is_published=True,
                                                        published_at=timezone.now(),
                                                        slug=slugify(cls.news_title))

        other_user_inst = User.objects.create_user(username=cls.other_username,
                                                   email=cls.other_user_email,
                                                   password=cls.other_user_password)
        UserProfile.objects.create(user=other_user_inst,
                                   telephone='1234',
                                   is_verified=True)

    def setUp(self):
        self.update_news_url = reverse('app_news:news_update', kwargs={'pk': self.published_news.id,
                                                                       'slug': self.published_news.slug})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированным пользователем.
        """

        response = self.client.get(self.update_news_url, follow=True)
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.update_news_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_other_user(self):
        """
        Тестирование GET запроса сторонним пользователем.
        """
        self.client.login(username=self.other_username, password=self.other_user_password)

        response = self.client.get(self.update_news_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsUpdateView.as_view().__name__)

    def test_get_request_news_owner(self):
        """
        Тестирование GET запроса владельцем новости.
        """
        self.client.login(username=self.news_owner_username, password=self.news_owner_user_password)

        response = self.client.get(self.update_news_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_update.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsUpdateView.as_view().__name__)

    def test_post_request_news_owner(self):
        """
        Тестирование POST запроса владельцем новости.
        """
        self.client.login(username=self.news_owner_username, password=self.news_owner_user_password)

        new_title = 'new title'
        new_content = 'new content'
        response = self.client.post(self.update_news_url,
                                    {'title': new_title,
                                     'content': new_content},
                                    follow=True)
        news_inst = models.News.objects.get(title=new_title)
        reversed_url = reverse('app_news:news_update', kwargs={'pk': news_inst.id,
                                                               'slug': news_inst.slug})
        self.assertEqual(news_inst.title, new_title)
        self.assertEqual(news_inst.content, new_content)
        self.assertEqual(news_inst.is_published, False)
        self.assertRedirects(response, reversed_url)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsUpdateView.as_view().__name__)


class NewsModerateViewTest(TestCase):
    """
    Тестирование представления NewsModerateView.
    """
    news_owner_username = 'test_username'
    news_owner_user_email = 'test@test.ru'
    news_owner_user_password = '123qweQWE'

    moderator_username = 'moderator_test_username'
    moderator_user_email = 'moderator_test@test.ru'
    moderator_user_password = '123qweQWE'

    news_title = 'Опубликованное название'
    news_content = 'Содержание Опубликованной новости' * 100

    @classmethod
    def setUpTestData(cls):
        verified_user_inst = User.objects.create_user(username=cls.news_owner_username,
                                                      email=cls.news_owner_user_email,
                                                      password=cls.news_owner_user_password)
        UserProfile.objects.create(user=verified_user_inst,
                                   telephone='123',
                                   is_verified=True)
        cls.not_published_news = models.News.objects.create(author=verified_user_inst,
                                                            title=cls.news_title,
                                                            content=cls.news_content,
                                                            published_at=timezone.now(),
                                                            slug=slugify(cls.news_title))

        moderator_user_inst = User.objects.create_user(username=cls.moderator_username,
                                                       email=cls.moderator_user_email,
                                                       password=cls.moderator_user_password)
        UserProfile.objects.create(user=moderator_user_inst,
                                   telephone='1234',
                                   is_verified=True)
        moder_group = Group.objects.get(name=MODERATOR_USER_GROUP_NAME)
        moderator_user_inst.groups.add(moder_group)

    def setUp(self):
        self.moderate_news_url = reverse('app_news:news_moderation', kwargs={'pk': self.not_published_news.id,
                                                                             'slug': self.not_published_news.slug})

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированного пользователя.
        """
        response = self.client.get(self.moderate_news_url, follow=True)
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.moderate_news_url}')
        self.assertEqual(response.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_request_not_moderate_user(self):
        """
        Тестирование GET запроса не модератором.
        """
        self.client.login(username=self.news_owner_username, password=self.news_owner_user_password)

        response = self.client.get(self.moderate_news_url, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsModerateView.as_view().__name__)

    def test_get_request_with_moderate_user(self):
        """
        Тестирование GET запроса модератором.
        """
        self.client.login(username=self.moderator_username, password=self.moderator_user_password)

        response = self.client.get(self.moderate_news_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_moderation.html')
        self.assertEqual(response.resolver_match.func.__name__, views.NewsModerateView.as_view().__name__)

    def test_post_request_with_moderate_user(self):
        """
        Тестирование POST запроса модератором.
        """
        self.client.login(username=self.moderator_username, password=self.moderator_user_password)
        self.assertFalse(self.not_published_news.is_published)

        response = self.client.post(self.moderate_news_url,
                                    {'is_published': True},
                                    follow=True)
        url = reverse('app_news:news_detail', kwargs={'pk': self.not_published_news.id,
                                                      'slug': self.not_published_news.slug})
        news_inst = models.News.objects.get(title=self.news_title)
        self.assertTrue(news_inst.is_published)
        self.assertRedirects(response, url)
        self.assertEqual(response.resolver_match.func.__name__, views.NewsDetailCommentCreateView.as_view().__name__)
