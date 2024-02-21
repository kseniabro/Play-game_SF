// Скрытие и отображение полей форм редактирования данных пользователя.
document.addEventListener("DOMContentLoaded", function () {
    let profileSettingsFields = document.querySelectorAll('div[change-profile-settings-field]')

    let onLinkClick = function (e) {
        // Скрытие полей форм редактирования.
        let profile_change_link = e.currentTarget,
            editableField = profile_change_link.parentNode.parentNode,
            hidden_form_field = editableField.querySelector('div[profile_change_form]'),
            site_lang = document.querySelector('html').lang,
            button_name = '';

        if (site_lang == 'en') {
            button_name = 'Change'
        }
        if (site_lang == 'ru') {
            button_name = 'Изменить'
        }
        if (site_lang == 'de') {
            button_name = 'Ändern'
        }

        if (!hidden_form_field.hidden) {
            hidden_form_field.hidden = true;
            editableField.classList.remove('profile-settings-field_inside-form-visible');
            editableField.classList.add('profile-settings-field_inside-form-hidden');
            profile_change_link.removeEventListener('click', onLinkClick);
            e.stopPropagation()
            editableField.addEventListener('click', onFieldClick);
            profile_change_link.innerText = button_name;
        }
    }

    let onFieldClick = function (e) {
        // Отображение полей формы редактирования.
        let editableField = e.currentTarget,
            hidden_form_field = editableField.querySelector('div[profile_change_form]'),
            profile_change_link = editableField.querySelector('a[profile_change_link]'),
            site_lang = document.querySelector('html').lang,
            button_name = '';

        if (site_lang == 'en') {
            button_name = 'Cancel'
        }
        if (site_lang == 'ru') {
            button_name = 'Отмена'
        }
        if (site_lang == 'de') {
            button_name = 'Annullierung'
        }

        if (hidden_form_field.hidden) {
            hidden_form_field.hidden = false;
            editableField.classList.add('profile-settings-field_inside-form-visible');
            editableField.classList.remove('profile-settings-field_inside-form-hidden');
            editableField.removeEventListener('click', onFieldClick);
            profile_change_link.addEventListener('click', onLinkClick);
            profile_change_link.innerText = button_name;
        }
    }

    for (let profileField of profileSettingsFields) {
        profileField.addEventListener('click', onFieldClick);
    }
})
