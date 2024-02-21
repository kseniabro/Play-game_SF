from django.forms import BaseForm


class ChangeIsValidFormMixin(BaseForm):
    """
    Форма добавляет CSS-класс 'invalid_field' полям, у которых есть ошибка.
    """

    def is_valid(self):
        result = super(ChangeIsValidFormMixin, self).is_valid()

        for field_name in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[field_name].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' invalid_field'})
        return result




