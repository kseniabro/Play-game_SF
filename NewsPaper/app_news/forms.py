from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from NewsPaper.app_news import models
from NewsPaper.project_modules.forms import ChangeIsValidFormMixin


class NewsForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма для создания новостной сводки.
    """
    class Meta:
        model = models.News
        exclude = ['author', 'is_published', 'slug', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-field',
                'aria-label': _('Введите название новости'),
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-field form-field_content',
                'aria-label': _('Введите комментарий'),
            }),
        }


class NewsModerateForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма для модерации новостной сводки, управление статусом is_published модели News.
    """

    class Meta:
        model = models.News
        fields = ['is_published']
        widgets = {
            'is_published': forms.CheckboxInput(attrs={
                'class': 'news-verified-status',
                'aria-label': _('Поменять статус публикации'),
                'title': _('Поменять статус публикации'),
            }),
        }


class CommentForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма для создания комментария к новостной сводке.
    """

    def __init__(self, user, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = models.Comment
        exclude = ['user', 'news']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'required': '',
                'class': 'form-field',
                'placeholder': _('Введите свое имя'),
                'aria-label': _('Введите свое имя'),
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-field form-field_content',
                'placeholder': _('Введите комментарий'),
                'aria-label': _('Введите комментарий'),
            }),
        }

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        user_name = cleaned_data['user_name']

        if not self.user.is_authenticated and not user_name:
            self.add_error('user_name', _('Необходимо ввести имя пользователя'))

        return cleaned_data


NewsModerateFormSet = modelformset_factory(models.News, form=NewsModerateForm)
