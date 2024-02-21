import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from NewsPaper.project_modules.forms import ChangeIsValidFormMixin
from NewsPaper.app_users import models


LOGIN_REGISTER_UPDATE_FIELD_CLASS = 'login-register-update-field'

PASSWORD_HELP_TEXT = _("Пароль не должен быть слишком похож на другую вашу личную информацию. Ваш "
                       "пароль должен содержать как минимум 8 символов. Такой пароль часто "
                       "используется. Пароль не может состоять только из цифр.")


class CleanedUserProfileTelephoneMixin:
    """
    Миксин для проверки поля telephone модели UserProfile.
    """

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        telephone_digits = re.sub(r'\D', '', telephone)

        if telephone.startswith('8'):
            telephone = f'+7{telephone_digits[1:]}'
        else:
            telephone = f'+{telephone_digits}'

        user_with_telephone = models.UserProfile.objects.filter(telephone=telephone)

        if user_with_telephone.exists():
            if user_with_telephone.filter(pk=self.instance.id).exists():
                error_message = _('Это ваш номер телефона, пожалуйста введите другой')
            else:
                error_message = _('Пользователь с таким номером уже существует')
            self.add_error('telephone', error_message)

        return telephone


class CleanedUserEmailMixin:
    """
    Миксин для проверки поля email модели User.
    """

    def clean_email(self):
        email = self.cleaned_data['email']
        users_with_email = User.objects.filter(email=email)

        if not email:
            self.add_error('email', _('Необходимо ввести адрес электронной почты'))
        elif users_with_email.exists():
            if users_with_email.filter(pk=self.instance.id).exists():
                error_message = _('Это ваш Email, пожалуйста введите другой')
            else:
                error_message = _('Пользователь с таким E-mail уже существует')
            self.add_error('email', error_message)

        return email


class AuthForm(AuthenticationForm, ChangeIsValidFormMixin):
    """
    Форма аутентификации пользователя.
    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': _('Введите логин'),
            'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS,
        }),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': _('Введите пароль'),
            'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS,
        }),
    )


class UserChangePasswordForm(PasswordChangeForm, ChangeIsValidFormMixin):
    """
    Форма смены пароля пользователя.
    """
    prefix = 'change_password_form'

    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].help_text = _('Введите ваш старый пароль')
        self.fields['new_password1'].help_text = PASSWORD_HELP_TEXT
        self.fields['new_password2'].help_text = _('Повторите пароль')

        for field in self.fields.values():
            field.widget.attrs.update({'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS,
                                       'title': field.help_text, })

        self.fields['old_password'].widget.attrs.update({'placeholder': _('Введите старый пароль'),
                                                         'aria-label': _('Введите старый пароль'), })
        self.fields['new_password1'].widget.attrs.update({'placeholder': _('Введите новый пароль'),
                                                          'aria-label': _('Введите новый пароль'), })
        self.fields['new_password2'].widget.attrs.update({'placeholder': _('Повторите пароль'),
                                                          'aria-label': _('Повторите пароль'), })


class RegisterForm(UserCreationForm, ChangeIsValidFormMixin, CleanedUserProfileTelephoneMixin, CleanedUserEmailMixin):
    """
    Форма регистрации пользователя.
    """
    telephone = forms.CharField(max_length=20,
                                required=True,
                                help_text=_('Введите ваш номер телефона'), )

    telephone.widget.attrs.update({'placeholder': _('Номер телефона'),
                                   'type': 'tel',
                                   'aria-label': _('Введите ваш номер телефона'),
                                   'data-tel-input': '', })

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].help_text = _('Адрес электронной почты должен содержать "@"')
        self.fields['password1'].help_text = PASSWORD_HELP_TEXT

        for field in self.fields.values():
            field.widget.attrs.update({'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS,
                                       'title': f'{field.help_text}', })

        self.fields['username'].widget.attrs.update({'placeholder': _('Логин'),
                                                     'aria-label': _('Введите ваш логин'), })
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail',
                                                  'aria-label': _('Введите ваш e-mail'), })
        self.fields['password1'].widget.attrs.update({'placeholder': _('Введите пароль'),
                                                      'aria-label': _('Введите пароль'), })
        self.fields['password2'].widget.attrs.update({'placeholder': _('Повторите пароль'),
                                                      'aria-label': _('Повторите пароль'), })

    class Meta:
        model = User
        fields = ('username', 'email', 'telephone', 'password1', 'password2',)


class UserProfileTelephoneForm(forms.ModelForm, ChangeIsValidFormMixin, CleanedUserProfileTelephoneMixin):
    """
    Форма смены телефона пользователя
    """
    prefix = 'telephone_form'

    def __init__(self, *args, **kwargs):
        super(UserProfileTelephoneForm, self).__init__(*args, **kwargs)

        self.fields['telephone'].widget.attrs.update({'placeholder': _('Введите новый номер телефона'),
                                                      'type': 'tel',
                                                      'aria-label': _('Введите ваш номер телефона'),
                                                      'title': _('Введите ваш номер телефона'),
                                                      'data-tel-input': '',
                                                      'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS, })

    class Meta:
        model = models.UserProfile
        fields = ('telephone',)


class UserProfileCityForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма смены города пользователя
    """
    prefix = 'city_form'

    def __init__(self, *args, **kwargs):
        super(UserProfileCityForm, self).__init__(*args, **kwargs)

        self.fields['city'].widget.attrs.update({'placeholder': _('Введите новый город'),
                                                 'aria-label': _('Введите новый город'),
                                                 'title': _('Введите новый город'),
                                                 'required': True,
                                                 'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS, })

    def clean_city(self):
        city = self.cleaned_data['city']

        if not city:
            self.add_error('city', _('Введите пожалуйста название города'))

        return city

    class Meta:
        model = models.UserProfile
        fields = ('city',)


class UserUsernameForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма смены имени пользователя
    """
    prefix = 'username_form'

    def __init__(self, *args, **kwargs):
        super(UserUsernameForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': _('Введите новый логин'),
                                                     'aria-label': _('Введите новый логин'),
                                                     'title': _('Введите новый логин'),
                                                     'required': True,
                                                     'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS, })

    class Meta:
        model = User
        fields = ('username',)


class UserEmailForm(forms.ModelForm, ChangeIsValidFormMixin, CleanedUserEmailMixin):
    """
    Форма смены e-mail пользователя
    """
    prefix = 'email_form'

    def __init__(self, *args, **kwargs):
        super(UserEmailForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'placeholder': _('Введите новый email'),
                                                  'aria-label': _('Введите новый email'),
                                                  'title': _('Введите новый email'),
                                                  'required': True,
                                                  'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS, })

    class Meta:
        model = User
        fields = ('email',)


class UserProfileVerificationForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма верификации пользователя
    """

    class Meta:
        model = models.UserProfile
        fields = ('is_verified',)
        widgets = {
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'user-verified-status',
                'aria-label': _('Поменять статус верификации'),
                'title': _('Поменять статус верификации'),
            }),
        }


UserProfileModerateFormSet = modelformset_factory(models.UserProfile, form=UserProfileVerificationForm)
