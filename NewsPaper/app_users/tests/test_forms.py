from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import password_validators_help_texts
from django.forms import TextInput, PasswordInput, CheckboxInput
from django.test import TestCase

from NewsPaper.app_users import forms, models
from NewsPaper.app_users.forms import LOGIN_REGISTER_UPDATE_FIELD_CLASS


User = get_user_model()


class AuthFormTest(TestCase):
    """
    Тестирование формы AuthForm.
    """

    def setUp(self):
        self.form = forms.AuthForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 2)

    def test_username_widget(self):
        """
        Тестирование widget у поля username
        """
        self.assertTrue(isinstance(self.form.fields['username'].widget, TextInput))

    def test_password_widget(self):
        """
        Тестирование widget у поля password
        """
        self.assertTrue(isinstance(self.form.fields['password'].widget, PasswordInput))

    def test_username_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля username
        """
        field = self.form.fields['username']
        self.assertEqual(field.widget.attrs['autofocus'], True)
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите логин')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_password_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля password
        """
        field = self.form.fields['password']
        self.assertEqual(field.widget.attrs['autocomplete'], 'current-password')
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите пароль')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)


class UserChangePasswordFormTest(TestCase):
    """
    Тестирование формы UserChangePasswordForm.
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
        self.form = forms.UserChangePasswordForm(user=self.user_inst)

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 3)

    def test_form_prefix(self):
        """
        Тестирование prefix у поля формы.
        """
        self.assertEqual(self.form.prefix, 'change_password_form')

    def test_old_password_help_text(self):
        """
        Тестирование help_text у поля old_password.
        """
        self.assertEqual(self.form.fields['old_password'].help_text, 'Введите ваш старый пароль')

    def test_new_password1_help_text(self):
        """
        Тестирование help_text у поля new_password1.
        """
        self.assertEqual(self.form.fields['new_password1'].help_text, ''.join(password_validators_help_texts()))

    def test_new_password2_help_text(self):
        """
        Тестирование help_text у поля new_password2.
        """
        self.assertEqual(self.form.fields['new_password2'].help_text, 'Повторите пароль')

    def test_old_password_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля old_password.
        """
        field = self.form.fields['old_password']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите старый пароль')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите старый пароль')
        self.assertEqual(field.widget.attrs['title'], 'Введите ваш старый пароль')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_new_password1_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля new_password1.
        """
        field = self.form.fields['new_password1']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите новый пароль')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите новый пароль')
        self.assertEqual(field.widget.attrs['title'], ''.join(password_validators_help_texts()))
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_new_password2_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля new_password2.
        """
        field = self.form.fields['new_password2']
        self.assertEqual(field.widget.attrs['placeholder'], 'Повторите пароль')
        self.assertEqual(field.widget.attrs['aria-label'], 'Повторите пароль')
        self.assertEqual(field.widget.attrs['title'], 'Повторите пароль')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_add_invalid_field_class(self):
        """
        Тестирование добавления класса к полям с ошибкой.
        """
        form = forms.UserChangePasswordForm(user=self.user_inst,
                                            data={'old_password': 'password'})
        self.assertFalse(form.is_valid())

        self.assertEqual(form.fields['old_password'].widget.attrs['class'],
                         f'{LOGIN_REGISTER_UPDATE_FIELD_CLASS} invalid_field')


class RegisterFormTest(TestCase):
    """
    Тестирование формы RegisterForm.
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephpone = '+788888'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User.objects.create_user(username=cls.username,
                                                 email=cls.user_email,
                                                 password=cls.user_password)
        models.UserProfile.objects.create(user=cls.user_inst,
                                          telephone=cls.telephpone,
                                          is_verified=True)

    def setUp(self):
        self.form = forms.RegisterForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 5)

    def test_telephone_help_text(self):
        """
        Тестирование help_text у поля telephone.
        """
        self.assertEqual(self.form.fields['telephone'].help_text, 'Введите ваш номер телефона')

    def test_telephone_max_length(self):
        """
        Тестирование max_length у поля telephone.
        """
        self.assertEqual(self.form.fields['telephone'].max_length, 20)

    def test_telephone_required(self):
        """
        Тестирование required у поля telephone.
        """
        self.assertEqual(self.form.fields['telephone'].required, True)

    def test_telephone_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля telephone.
        """
        field = self.form.fields['telephone']
        self.assertEqual(field.widget.attrs['placeholder'], 'Номер телефона')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите ваш номер телефона')
        self.assertEqual(field.widget.attrs['title'], 'Введите ваш номер телефона')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)
        self.assertEqual(field.widget.attrs['type'], 'tel')
        self.assertEqual(field.widget.attrs['data-tel-input'], '')

    def test_email_help_text(self):
        """
        Тестирование help_text у поля email.
        """
        self.assertEqual(self.form.fields['email'].help_text, 'Адрес электронной почты должен содержать "@"')

    def test_email_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля email.
        """
        field = self.form.fields['email']
        self.assertEqual(field.widget.attrs['placeholder'], 'E-mail')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите ваш e-mail')
        self.assertEqual(field.widget.attrs['title'], 'Адрес электронной почты должен содержать "@"')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_password1_help_text(self):
        """
        Тестирование help_text у поля password1.
        """
        self.assertEqual(self.form.fields['password1'].help_text, ''.join(password_validators_help_texts()))

    def test_password1_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля password1.
        """
        field = self.form.fields['password1']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите пароль')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите пароль')
        self.assertEqual(field.widget.attrs['title'], ''.join(password_validators_help_texts()))
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_username_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля username.
        """
        field = self.form.fields['username']
        self.assertEqual(field.widget.attrs['placeholder'], 'Логин')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите ваш логин')
        self.assertEqual(field.widget.attrs['title'], field.help_text)
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_password2_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля password2.
        """
        field = self.form.fields['password2']
        self.assertEqual(field.widget.attrs['placeholder'], 'Повторите пароль')
        self.assertEqual(field.widget.attrs['aria-label'], 'Повторите пароль')
        self.assertEqual(field.widget.attrs['title'], field.help_text)
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, User)

    def test_email_valid(self):
        """
        Тестирование валидности поля email при пустом значении.
        """
        form = forms.RegisterForm(data={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('email').as_text(), '* Необходимо ввести адрес электронной почты')

    def test_email_valid_2(self):
        """
        Тестирование валидности поля email при повторяющемся значении.
        """
        form = forms.RegisterForm(data={'email': self.user_email})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('email').as_text(), '* Пользователь с таким E-mail уже существует')

    def test_telephone_valid(self):
        """
        Тестирование валидности поля telephone при повторяющемся значении.
        """
        form = forms.RegisterForm(data={'telephone': self.telephpone})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('telephone').as_text(), '* Пользователь с таким номером уже существует')

    def test_telephone_correct(self):
        """
        Тестирование корректировки номера телефона перед сохранением в базу.
        """
        telephone = '123456789'

        form = forms.RegisterForm(data={'telephone': f'{telephone}qwe'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.cleaned_data['telephone'], f'+{telephone}')

    def test_telephone_correct_2(self):
        """
        Тестирование корректировки номера телефона перед сохранением в базу если он начинается с 8.
        """
        telephone = '823456789'

        form = forms.RegisterForm(data={'telephone': f'{telephone}qwe'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.cleaned_data['telephone'], f'+7{telephone[1:]}')


class UserProfileTelephoneFormTest(TestCase):
    """
    Тестирование формы UserProfileTelephoneForm.
    """

    def setUp(self):
        self.form = forms.UserProfileTelephoneForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 1)

    def test_form_prefix(self):
        """
        Тестирование prefix у поля формы.
        """
        self.assertEqual(self.form.prefix, 'telephone_form')

    def test_telephone_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля telephone.
        """
        field = self.form.fields['telephone']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите новый номер телефона')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите ваш номер телефона')
        self.assertEqual(field.widget.attrs['title'], 'Введите ваш номер телефона')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)
        self.assertEqual(field.widget.attrs['type'], 'tel')
        self.assertEqual(field.widget.attrs['data-tel-input'], '')

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, models.UserProfile)


class UserProfileCityFormTest(TestCase):
    """
    Тестирование формы UserProfileCityForm.
    """

    def setUp(self):
        self.form = forms.UserProfileCityForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 1)

    def test_form_prefix(self):
        """
        Тестирование prefix у поля формы.
        """
        self.assertEqual(self.form.prefix, 'city_form')

    def test_city_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля city.
        """
        field = self.form.fields['city']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите новый город')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите новый город')
        self.assertEqual(field.widget.attrs['title'], 'Введите новый город')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)
        self.assertEqual(field.widget.attrs['required'], True)

    def test_telephone_valid(self):
        """
        Тестирование валидности пустого поля city.
        """
        form = forms.UserProfileCityForm(data={'city': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('city').as_text(), '* Введите пожалуйста название города')

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, models.UserProfile)


class UserUsernameFormTest(TestCase):
    """
    Тестирование формы UserUsernameForm.
    """

    def setUp(self):
        self.form = forms.UserUsernameForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 1)

    def test_form_prefix(self):
        """
        Тестирование prefix у поля формы.
        """
        self.assertEqual(self.form.prefix, 'username_form')

    def test_city_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля city.
        """
        field = self.form.fields['username']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите новый логин')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите новый логин')
        self.assertEqual(field.widget.attrs['title'], 'Введите новый логин')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)
        self.assertEqual(field.widget.attrs['required'], True)

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, User)


class UserEmailFormTest(TestCase):
    """
    Тестирование формы UserEmailForm.
    """

    def setUp(self):
        self.form = forms.UserEmailForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 1)

    def test_form_prefix(self):
        """
        Тестирование prefix у поля формы.
        """
        self.assertEqual(self.form.prefix, 'email_form')

    def test_city_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля city.
        """
        field = self.form.fields['email']
        self.assertEqual(field.widget.attrs['placeholder'], 'Введите новый email')
        self.assertEqual(field.widget.attrs['aria-label'], 'Введите новый email')
        self.assertEqual(field.widget.attrs['title'], 'Введите новый email')
        self.assertEqual(field.widget.attrs['class'], LOGIN_REGISTER_UPDATE_FIELD_CLASS)
        self.assertEqual(field.widget.attrs['required'], True)

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, User)


class UserProfileVerificationFormTest(TestCase):
    """
    Тестирование формы UserProfileVerificationForm.
    """

    def setUp(self):
        self.form = forms.UserProfileVerificationForm()

    def test_count_form_fields(self):
        """
        Тестирование количества полей у формы.
        """
        self.assertEqual(len(self.form.fields), 1)

    def test_is_verified_widget(self):
        """
        Тестирование widget у поля city.
        """
        self.assertTrue(isinstance(self.form.fields['is_verified'].widget, CheckboxInput))

    def test_city_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля city.
        """
        field = self.form.fields['is_verified']
        self.assertEqual(field.widget.attrs['aria-label'], 'Поменять статус верификации')
        self.assertEqual(field.widget.attrs['title'], 'Поменять статус верификации')
        self.assertEqual(field.widget.attrs['class'], 'user-verified-status')

    def test_form_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.form.Meta.model, models.UserProfile)


class UserProfileModerateFormSetTest(TestCase):
    """
    Тестирование формы NewsModerateFormSet.
    """

    def setUp(self):
        self.formset = forms.UserProfileModerateFormSet

    def test_formset_model(self):
        """
        Тестирование модели с которой работает форма.
        """
        self.assertEqual(self.formset.model, models.UserProfile)

    def test_formset_form_name(self):
        """
        Тестирование формы с которой работает набор форм.
        """
        form_name = forms.UserProfileVerificationForm.Meta.model.__name__ + 'Form'
        self.assertEqual(self.formset.form.__name__, form_name)
