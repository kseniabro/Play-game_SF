from django.contrib.auth import get_user_model
from django.db.models import SET_NULL, CASCADE
from django.test import TestCase
from django.urls import reverse

from NewsPaper.app_news import models
from NewsPaper.app_news.permissions import PUBLISH_NEWS_PERM_CODE_NAME
from NewsPaper.app_users.models import UserProfile

User = get_user_model()


class NewsModelTest(TestCase):
    """
    Тестирование модели News.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        UserProfile.objects.create(user=user_inst,
                                   telephone='123',
                                   is_verified=True)
        cls.news_inst = models.News.objects.create(id=1,
                                                   author=user_inst,
                                                   title='title',
                                                   content='content')

    def test_author_verbose_name(self):
        """
        Тестирование verbose_name у поля author.
        """
        self.assertEquals(self.news_inst._meta.get_field('author').verbose_name, 'Пользователь')

    def test_author_related_model(self):
        """
        Тестирование related_model у поля author.
        """

        self.assertEquals(self.news_inst._meta.get_field('author').related_model, User)

    def test_author_on_delete(self):
        """
        Тестирование on_delete у поля author.
        """
        self.assertEquals(self.news_inst._meta.get_field('author').remote_field.on_delete, SET_NULL)

    def test_author_related_name(self):
        """
        Тестирование related_name у поля author.
        """
        self.assertEquals(self.news_inst._meta.get_field('author').remote_field.related_name, 'news')

    def test_author_null(self):
        """
        Тестирование null у поля author.
        """
        self.assertEquals(self.news_inst._meta.get_field('author').null, True)

    def test_title_verbose_name(self):
        """
        Тестирование verbose_name у поля title.
        """
        field_label = self.news_inst._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_title_max_length(self):
        """
        Тестирование max_length у поля title.
        """
        self.assertEquals(self.news_inst._meta.get_field('title').max_length, 100)

    def test_title_db_index(self):
        """
        Тестирование db_index у поля title.
        """
        self.assertEquals(self.news_inst._meta.get_field('title').db_index, True)

    def test_content_verbose_name(self):
        """
        Тестирование verbose_name у поля content.
        """
        self.assertEquals(self.news_inst._meta.get_field('content').verbose_name, 'Содержание')

    def test_created_at_verbose_name(self):
        """
        Тестирование verbose_name у поля created_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('created_at').verbose_name, 'Дата создания')

    def test_created_at_auto_now_add(self):
        """
        Тестирование auto_now_add у поля created_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('created_at').auto_now_add, True)

    def test_published_at_verbose_name(self):
        """
        Тестирование verbose_name у поля published_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('published_at').verbose_name, 'Дата публикации')

    def test_published_at_null(self):
        """
        Тестирование null у поля published_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('published_at').null, True)

    def test_published_at_blank(self):
        """
        Тестирование blank у поля published_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('published_at').blank, True)

    def test_edited_at_verbose_name(self):
        """
        Тестирование verbose_name у поля edited_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('edited_at').verbose_name, 'Дата редактирования')

    def test_edited_at_auto_now(self):
        """
        Тестирование auto_now у поля edited_at.
        """
        self.assertEquals(self.news_inst._meta.get_field('edited_at').auto_now, True)

    def test_is_published_verbose_name(self):
        """
        Тестирование verbose_name у поля is_published.
        """
        self.assertEquals(self.news_inst._meta.get_field('is_published').verbose_name, 'Статус публикации')

    def test_is_published_db_index(self):
        """
        Тестирование db_index у поля is_published.
        """
        self.assertEquals(self.news_inst._meta.get_field('is_published').db_index, True)

    def test_is_published_default(self):
        """
        Тестирование default у поля is_published.
        """
        self.assertEquals(self.news_inst._meta.get_field('is_published').default, False)

    def test_slug_verbose_name(self):
        """
        Тестирование verbose_name у поля slug.
        """
        self.assertEquals(self.news_inst._meta.get_field('slug').verbose_name, 'slug-url')

    def test_model_verbose_name(self):
        """
        Тестирование verbose_name у модели.
        """
        self.assertEquals(self.news_inst._meta.verbose_name, 'Новость')

    def test_model_verbose_name_plural(self):
        """
        Тестирование verbose_name_plural у модели.
        """
        self.assertEquals(self.news_inst._meta.verbose_name_plural, 'Новости')

    def test_model_ordering(self):
        """
        Тестирование ordering у модели.
        """
        self.assertEquals(self.news_inst._meta.ordering, ['-created_at'])

    def test_model_permissions(self):
        """
        Тестирование permissions у модели.
        """
        self.assertEquals(self.news_inst._meta.permissions, (
            (PUBLISH_NEWS_PERM_CODE_NAME, "Может публиковать новости"),
        ))

    def test_get_absolute_url(self):
        """
        Тестирование метода get_absolute_url.
        """
        self.assertEquals(self.news_inst.get_absolute_url(),
                          reverse('app_news:news_detail', kwargs={'pk': str(self.news_inst.id),
                                                                  'slug': self.news_inst.slug}))

    def test_str_represent_name(self):
        """
        Тестирование текстового представления новости.
        """
        self.assertEquals(f'{self.news_inst.title}', str(self.news_inst))


class CommentModelTest(TestCase):
    """
    Тестирование модели Comment.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User.objects.create_user(username=cls.username,
                                             email=cls.user_email,
                                             password=cls.user_password)
        UserProfile.objects.create(user=user_inst,
                                   telephone='123',
                                   is_verified=True)
        news_inst = models.News.objects.create(id=1,
                                               author=user_inst,
                                               title='title',
                                               content='content')
        cls.comment_inst = models.Comment.objects.create(id=1,
                                                         user=user_inst,
                                                         user_name=user_inst.username,
                                                         text='text',
                                                         news=news_inst)

        cls.anonymous_comment_inst = models.Comment.objects.create(id=2,
                                                                   user_name='some_username',
                                                                   text='text',
                                                                   news=news_inst)

    def test_user_verbose_name(self):
        """
        Тестирование verbose_name у поля user.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user').verbose_name, 'Пользователь')

    def test_user_related_model(self):
        """
        Тестирование related_model у поля user.
        """

        self.assertEquals(self.comment_inst._meta.get_field('user').related_model, User)

    def test_user_on_delete(self):
        """
        Тестирование on_delete у поля user.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user').remote_field.on_delete, CASCADE)

    def test_user_related_name(self):
        """
        Тестирование related_name у поля user.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user').remote_field.related_name, 'comments')

    def test_user_null(self):
        """
        Тестирование null у поля user.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user').null, True)

    def test_user_blank(self):
        """
        Тестирование blank у поля user.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user').blank, True)

    def test_user_name_verbose_name(self):
        """
        Тестирование verbose_name у поля user_name.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user_name').verbose_name, 'Имя пользователя')

    def test_user_name_max_length(self):
        """
        Тестирование max_length у поля user_name.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user_name').max_length, 100)

    def test_user_name_db_index(self):
        """
        Тестирование db_index у поля user_name.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user_name').db_index, True)

    def test_user_name_blank(self):
        """
        Тестирование blank у поля user_name.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user_name').blank, True)

    def test_user_name_null(self):
        """
        Тестирование null у поля user_name.
        """
        self.assertEquals(self.comment_inst._meta.get_field('user_name').null, True)

    def test_text_verbose_name(self):
        """
        Тестирование verbose_name у поля user_name.
        """
        self.assertEquals(self.comment_inst._meta.get_field('text').verbose_name, 'Комментарий')

    def test_news_verbose_name(self):
        """
        Тестирование verbose_name у поля news.
        """
        self.assertEquals(self.comment_inst._meta.get_field('news').verbose_name, 'Новость')

    def test_news_related_model(self):
        """
        Тестирование related_model у поля news.
        """

        self.assertEquals(self.comment_inst._meta.get_field('news').related_model, models.News)

    def test_news_on_delete(self):
        """
        Тестирование on_delete у поля news.
        """
        self.assertEquals(self.comment_inst._meta.get_field('news').remote_field.on_delete, CASCADE)

    def test_news_related_name(self):
        """
        Тестирование related_name у поля news.
        """
        self.assertEquals(self.comment_inst._meta.get_field('news').remote_field.related_name, 'comments')

    def test_created_at_verbose_name(self):
        """
        Тестирование verbose_name у поля created_at.
        """
        self.assertEquals(self.comment_inst._meta.get_field('created_at').verbose_name, 'Дата создания')

    def test_created_at_auto_now_add(self):
        """
        Тестирование auto_now_add у поля created_at.
        """
        self.assertEquals(self.comment_inst._meta.get_field('created_at').auto_now_add, True)

    def test_created_at_db_index(self):
        """
        Тестирование db_index у поля created_at.
        """
        self.assertEquals(self.comment_inst._meta.get_field('created_at').db_index, True)

    def test_model_verbose_name(self):
        """
        Тестирование verbose_name у модели.
        """
        self.assertEquals(self.comment_inst._meta.verbose_name, 'Комментарий')

    def test_model_verbose_name_plural(self):
        """
        Тестирование verbose_name_plural у модели.
        """
        self.assertEquals(self.comment_inst._meta.verbose_name_plural, 'Комментарии')

    def test_str_represent_name(self):
        """
        Тестирование текстового представления комментария.
        """
        self.assertEquals(self.comment_inst.user.username, str(self.comment_inst))

    def test_str_anonymous_represent_name(self):
        """
        Тестирование текстового представления анонимного комментария.
        """
        self.assertEquals(f'{self.anonymous_comment_inst.user_name} (аноним)', str(self.anonymous_comment_inst))
