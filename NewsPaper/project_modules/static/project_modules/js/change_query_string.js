function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}


export function getQueryStrings(string) {
    // Получение параметров запроса и создание словаря параметров {имя_параемтра': 'значение_параметра'}.
    let assoc  = {},
        decode = function (s) { return decodeURIComponent(s.replace(/\+/g, " ")); },
        queryString = location.search.substring(1);

    if (string) queryString = string
    let keyValues = queryString.split('&');

    for (let keyVal of keyValues) {
        let key = keyVal.split('=');
        if (key.length > 1) {
            assoc[decode(key[0])] = decode(key[1]);
        }
    }

    return assoc;
}


export  function getNewQuery(new_params) {
    // Замена параметров запроса на переданные и составление новой строки параметров запроса.
    let querystring = getQueryStrings(),
        new_query = '';

    for (let param_key in new_params) {
        if (new_params[param_key]) {
            querystring[param_key] = new_params[param_key]
        } else {
            delete querystring[param_key];
        }
    }

    let count_query_keys = Object.keys(querystring).length,
        counter = 0;
    if (querystring) {
        new_query += '?'
        for (let key in querystring) {
            counter += 1
            new_query += key + '=' +querystring[key]
            if (counter != count_query_keys) new_query += '&'
        }
    }
    return new_query
}


export function addCommonFilters(object_name, filter_names_list) {
    // Установка фильтров для отображаемых объектов.
    let news_per_page = document.querySelector(`select[name="${object_name}_per_page"]`),
        all_query_params = {},

        news_filter_apply_button = document.querySelector(`button[id="${object_name}_filter_apply"]`),
        news_filter_delete_button = document.querySelector(`button[id="${object_name}_filter_delete"]`),

        current_query_params = getQueryStrings();

    for (let filter_name of filter_names_list) {
        all_query_params[filter_name] = document.querySelector(`input[name="${filter_name}"]`)
    }

    function setFiltervalues() {
        for (let filter_name in all_query_params) {
            all_query_params[filter_name] = all_query_params[filter_name].value
        }
        all_query_params['page'] = NaN
    }

    news_filter_delete_button.onclick = function () {
        // Отчистка всех фильтров.
        for (let filter_name in all_query_params) {
            all_query_params[filter_name] = NaN
        }
        document.location.href = getNewQuery(all_query_params);
    }

    news_filter_apply_button.onclick = function () {
        // Применение установленных фильтров.
        setFiltervalues()

        document.location.href = getNewQuery(all_query_params);
    }

    news_per_page.onchange = function() {
        // Управление колличеством отображаемых объектов на странице.
        setFiltervalues()

        document.cookie = `${object_name}_per_page=` + encodeURIComponent(this.value)
        document.location.href = getNewQuery(all_query_params);
    }

    // Получаем значения фильтров из запроса и устанавливаем эти значения в свои поля.
    for (let filter_name in all_query_params) {
        if (filter_name in current_query_params) {
            all_query_params[filter_name].value = current_query_params[filter_name]
        }
    }

    for (let option of news_per_page.options) {
        if (option.value == getCookie(`${object_name}_per_page`)){
            option.selected = true
        }
    }
}


export function addStatusFilter(displayed_param_name) {
    // Управление отображением объектов по своему статусу активности.
    let news_activity_filter_links = document.querySelectorAll('.object-filters__status-fields'),
        query_params = getQueryStrings();

    let make_check_box_checked = function (check_box, news_link) {
        check_box.checked = true
        news_link.classList.add('object-filters__status-fields_checked')
    }

    if (!(displayed_param_name in query_params)) {
        let check_box = document.querySelector('.object-filters__status-fields input[value="all"]'),
            news_link = check_box.parentNode

        make_check_box_checked(check_box, news_link)
    }

    for (let news_link of news_activity_filter_links) {
        let check_box = news_link.querySelector('input'),
            params = {
                [displayed_param_name]: check_box.value,
            };

        news_link.href = getNewQuery(params)
        if (check_box.value == query_params[displayed_param_name]) {
            make_check_box_checked(check_box, news_link)
        }
    }
}