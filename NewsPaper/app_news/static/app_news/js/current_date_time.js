setInterval(function () {
    // Показывает текущее время пользователя сайта.
    let cur_dt = new Date();
    document.getElementById('current_date_time').innerHTML =
        cur_dt.toLocaleString('ru-RU').replace(',', ' ');
}, 1000);
