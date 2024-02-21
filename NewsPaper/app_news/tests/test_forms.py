from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.forms import TextInput, Textarea, CheckboxInput
from django.test import TestCase

from NewsPaper.app_news import forms, models


User = get_user_model()


class NewsFormTest(TestCase):
    """
    Тестирование формы NewsForm.
    """

    def setUp(self):
        self.form = forms.NewsForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 2)

    def test_title_widget(self):
        """
        Тестирование widget у поля title
        """
        self.assertTrue(isinstance(self.form.fields['title'].widget, TextInput))

    def test_content_widget(self):
        """
        Тестирование widget у поля content
        """
        self.assertTrue(isinstance(self.form.fields['content'].widget, Textarea))

    def test_title_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля title
        """
        self.assertEqual(self.form.fields['title'].widget.attrs['class'], 'form-field')
        self.assertEqual(self.form.fields['title'].widget.attrs['aria-label'], 'Введите название новости')

    def test_content_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля content
        """
        self.assertEqual(self.form.fields['content'].widget.attrs['class'], 'form-field form-field_content')
        self.assertEqual(self.form.fields['content'].widget.attrs['aria-label'], 'Введите комментарий')

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, models.News)


class NewsModerateFormTest(TestCase):
    """
    Тестирование формы NewsModerateForm.
    """

    def setUp(self):
        self.form = forms.NewsModerateForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 1)

    def test_is_published_widget(self):
        """
        Тестирование widget у поля is_published
        """
        self.assertTrue(isinstance(self.form.fields['is_published'].widget, CheckboxInput))

    def test_is_published_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля is_published
        """
        self.assertEqual(self.form.fields['is_published'].widget.attrs['class'], 'news-verified-status')
        self.assertEqual(self.form.fields['is_published'].widget.attrs['aria-label'], 'Поменять статус публикации')
        self.assertEqual(self.form.fields['is_published'].widget.attrs['title'], 'Поменять статус публикации')

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, models.News)


class CommentFormTest(TestCase):
    """
    Тестирование формы CommentForm.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User.objects.create_user(username=cls.username,
                                                 email=cls.user_email,
                                                 password=cls.user_password)

    def setUp(self):
        self.form = forms.CommentForm(user=self.user_inst)

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 2)

    def test_user_name_widget(self):
        """
        Тестирование widget у поля user_name
        """
        self.assertTrue(isinstance(self.form.fields['user_name'].widget, TextInput))

    def test_text_widget(self):
        """
        Тестирование widget у поля text
        """
        self.assertTrue(isinstance(self.form.fields['text'].widget, Textarea))

    def test_user_name_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля user_name
        """
        self.assertEqual(self.form.fields['user_name'].widget.attrs['class'], 'form-field')
        self.assertEqual(self.form.fields['user_name'].widget.attrs['aria-label'], 'Введите свое имя')
        self.assertEqual(self.form.fields['user_name'].widget.attrs['placeholder'], 'Введите свое имя')

    def test_text_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля text
        """
        self.assertEqual(self.form.fields['text'].widget.attrs['class'], 'form-field form-field_content')
        self.assertEqual(self.form.fields['text'].widget.attrs['aria-label'], 'Введите комментарий')
        self.assertEqual(self.form.fields['text'].widget.attrs['placeholder'], 'Введите комментарий')

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, models.Comment)

    def test_form_valid_with_auth_user(self):
        """
        Тестирование валидности формы с аутентифицированным пользователем.
        """
        form = forms.CommentForm(user=self.user_inst,
                                 data={'text': 'comment text'})
        self.assertTrue(form.is_valid())

    def test_form_valid_with_not_auth_user_without_user_name(self):
        """
        Тестирование валидности формы с не аутентифицированным пользователем без поля user_name.
        """
        form = forms.CommentForm(user=AnonymousUser(),
                                 data={'text': 'comment text'})
        self.assertFalse(form.is_valid())

    def test_form_valid_with_not_auth_user_with_user_name(self):
        """
        Тестирование валидности формы с не аутентифицированным пользователем с корректными данными.
        """
        form = forms.CommentForm(user=AnonymousUser(),
                                 data={'text': 'comment text',
                                       'user_name': 'user name'})
        self.assertTrue(form.is_valid())


class NewsModerateFormSetTest(TestCase):
    """
    Тестирование формы NewsModerateFormSet.
    """

    def setUp(self):
        self.formset = forms.NewsModerateFormSet

    def test_formset_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.formset.model, models.News)

    def test_formset_form_name(self):
        """
        Тестирование формы с которой работает набор форм.
        """
        form_name = forms.NewsModerateForm.Meta.model.__name__ + 'Form'
        self.assertEqual(self.formset.form.__name__, form_name)
