document.addEventListener("DOMContentLoaded", function () {
    // Запрос подтверждения в случае обновления новости.
    let button_confirm = document.getElementById("change-news-confirm-button"),
        button_no = document.getElementById("change-news-confirm-button-no"),
        field_confirm = document.querySelector("div.update-news__confirm-wrap");



    let onButtonFieldClick = function (e){
        if (e.target == this) {
            field_confirm.style.display = 'none'
        }
    }

    if (button_confirm) {
        button_confirm.addEventListener('click', function (){
        field_confirm.style.display = 'flex'
        });

        button_no.addEventListener('click', onButtonFieldClick);

        field_confirm.addEventListener('click', onButtonFieldClick);
    }
})
