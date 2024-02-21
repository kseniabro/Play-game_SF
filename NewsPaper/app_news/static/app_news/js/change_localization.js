document.addEventListener("DOMContentLoaded", function () {
    // Переключение языка сайта.
    let select_obj = document.querySelector('select[name="language"]'),
        change_lang_form = document.querySelector('form[name="setLang"]');

    select_obj.addEventListener('change', function () {
        change_lang_form.submit()
    })
});