// Маска для поля ввода телефонного номера.
document.addEventListener("DOMContentLoaded", function () {
    let phoneInputs = document.querySelectorAll('input[data-tel-input]');

    let getInputNumbersValue = function (input) {
        // Получить чистый номер из цифр.
        return input.value.replace(/\D/g, '');
    }

    let getInputValueWithoutSeparators = function (text) {
        //Получить строку без разделителей номера.
        return text.replace(/[\s()-]/g, '');
    }

    let getFormattedInputValue = function (number) {
        // Получить номер с маской.
        let formattedInputValue = "";

        if (["7", "8", "9"].indexOf(number[0]) > -1) {
            if (number[0] == "9") number = "7" + number;
            let firstSymbols = (number[0] == "8") ? "8" : "+7";
            formattedInputValue = firstSymbols + " ";
            if (number.length > 1) {
                formattedInputValue += '(' + number.substring(1, 4);
            }
            if (number.length >= 5) {
                formattedInputValue += ') ' + number.substring(4, 7);
            }
            if (number.length >= 8) {
                formattedInputValue += '-' + number.substring(7, 9);
            }
            if (number.length >= 10) {
                formattedInputValue += '-' + number.substring(9, 11);
            }
        } else {
            formattedInputValue = '+' + number;
        }
        return formattedInputValue
    }

    let onPhonePaste = function (e) {
        // Запрещает вставлять нечисловые символы.
        let pasted = e.clipboardData || window.clipboardData;

        if (pasted) {
            let pastedText = getInputValueWithoutSeparators(pasted.getData('Text'));

            if (/[^0-9+]/g.test(pastedText)) {
                e.preventDefault();
            } else {
                e.preventDefault();
                window.document.execCommand('insertText', false, pastedText);
            }
        }
    }

    let onPhoneInput = function (e) {
        // Применить маску к номеру в поле ввода.
        let input = e.target,
            inputNumbersValue = getInputNumbersValue(input),
            selectionStart = input.selectionStart;

        if (input.value.length != selectionStart) return;

        if (["+"].indexOf(input.value[0]) > -1) {
            if (inputNumbersValue[0] != '7') {
                input.value = '+' + inputNumbersValue;
            } else {
                input.value = getFormattedInputValue(inputNumbersValue, input);
            }
        } else {
            input.value = getFormattedInputValue(inputNumbersValue, input);
        }
    }

    let onPhoneKeyDown = function (e) {
        // Обработка события нажатия на клавишу.
        let input = e.target,
            inputNumbersValue = getInputNumbersValue(input),
            inputLength = inputNumbersValue.length;

            // Отчистка input после удаления последнего символа.
        if ((e.keyCode == 8 || e.keyCode == 46) && (inputLength == 1 || input.value == '+')) {
             e.target.value = "";
        }

            // Разрешаем: backspace, delete, tab и escape.
        if ( e.keyCode == 46 || e.keyCode == 8 || e.keyCode == 9 || e.keyCode == 27 ||
            // Разрешаем: Ctrl+A Ctrl+C Ctrl+V.
            (e.keyCode == 65 && e.ctrlKey === true) ||
            (e.keyCode == 67 && e.ctrlKey === true) ||
            (e.keyCode == 86 && e.ctrlKey === true) ||
            // Разрешаем: +
            (e.keyCode == 107 || (e.keyCode == 187 && e.shiftKey === true))||
            // Разрешаем: home, end, влево, вправо.
            (e.keyCode >= 35 && e.keyCode <= 39)) {
        } else {
            // Запрещаем все, кроме цифр на основной клавиатуре, а так же Num-клавиатуре.
            if ((e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105 )) {
                e.preventDefault();
            }
        }
    }
    for (let phoneInput of phoneInputs) {
        phoneInput.addEventListener('keydown', onPhoneKeyDown);
        phoneInput.addEventListener('input', onPhoneInput, false);
        phoneInput.addEventListener('paste', onPhonePaste, false);
    }
})
