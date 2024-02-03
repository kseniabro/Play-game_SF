from bot_zoo.texts.animals_text import *

from bot_zoo.keyboards.quiz_results_kb import (
    inline_keyboard_result_1,
    inline_keyboard_result_2,
    inline_keyboard_result_3,
    inline_keyboard_result_4,
    inline_keyboard_result_5,
    inline_keyboard_result_6,
    inline_keyboard_result_7,
    inline_keyboard_result_8,
    inline_keyboard_result_9,
    inline_keyboard_result_10,
    inline_keyboard_result_11,
)


ALL_ANIMALS = {

    'ANIMAL_1': {
        'ANIMAL_NAME': 'Бинтуронг',
        'ANIMAL_IMAGE': 'images/binturong.jpg',
        'ANIMAL_KB': inline_keyboard_result_1,
        'ANIMAL_DESCRIPTION': ANIMAL_1_TEXT,
        'ANIMAL_QUALITIES': [],
    },

    'ANIMAL_2': {
        'ANIMAL_NAME': 'Капибара',
        'ANIMAL_IMAGE': 'images/kapibara.jpg',
        'ANIMAL_KB': inline_keyboard_result_2,
        'ANIMAL_DESCRIPTION': ANIMAL_2_TEXT,
        'ANIMAL_QUALITIES': [
            'спокойствие',
            'скрытность',
        ],
    },

    'ANIMAL_3': {
        'ANIMAL_NAME': 'Большая панда',
        'ANIMAL_IMAGE': 'images/big-panda.jpg',
        'ANIMAL_KB': inline_keyboard_result_3,
        'ANIMAL_DESCRIPTION': ANIMAL_3_TEXT,
        'ANIMAL_QUALITIES': [
            'спокойствие',
            'неуклюжесть',
        ],
    },

    'ANIMAL_4': {
        'ANIMAL_NAME': 'Никобарский голубь',
        'ANIMAL_IMAGE': 'images/nikobar-pigeon.jpg',
        'ANIMAL_KB': inline_keyboard_result_4,
        'ANIMAL_DESCRIPTION': ANIMAL_4_TEXT,
        'ANIMAL_QUALITIES': [
            'редкость',
            'стадность',
        ],
    },


    'ANIMAL_5': {
        'ANIMAL_NAME': 'Медоед',
        'ANIMAL_IMAGE': 'images/honey-eater.jpg',
        'ANIMAL_KB': inline_keyboard_result_5,
        'ANIMAL_DESCRIPTION': ANIMAL_5_TEXT,
        'ANIMAL_QUALITIES': [
            'безбашенность',
            'храбрость',
        ],
    },


    'ANIMAL_6': {
        'ANIMAL_NAME': 'Японский макак',
        'ANIMAL_IMAGE': 'images/japan-makak.jpg',
        'ANIMAL_KB': inline_keyboard_result_6,
        'ANIMAL_DESCRIPTION': ANIMAL_6_TEXT,
        'ANIMAL_QUALITIES': [
            'стадность',
            'ловкость',
        ],
    },


    'ANIMAL_7': {
        'ANIMAL_NAME': 'Ягуарунди',
        'ANIMAL_IMAGE': 'images/yaguarundi.jpg',
        'ANIMAL_KB': inline_keyboard_result_7,
        'ANIMAL_DESCRIPTION': ANIMAL_7_TEXT,
        'ANIMAL_QUALITIES': [
            'скорость',
            'храбрость',
        ],
    },


    'ANIMAL_8': {
        'ANIMAL_NAME': 'Ушастый ёж',
        'ANIMAL_IMAGE': 'images/big-ear-hedgehog.jpg',
        'ANIMAL_KB': inline_keyboard_result_8,
        'ANIMAL_DESCRIPTION': ANIMAL_8_TEXT,
        'ANIMAL_QUALITIES': [
            'теплолюбивость',
            'одиночка',
        ],
    },


    'ANIMAL_9': {
        'ANIMAL_NAME': 'Заяц беляк',
        'ANIMAL_IMAGE': 'images/white-rabbit.jpg',
        'ANIMAL_KB': inline_keyboard_result_9,
        'ANIMAL_DESCRIPTION': ANIMAL_9_TEXT,
        'ANIMAL_QUALITIES': [
            'ловкость',
            'одиночка',
        ],
    },


    'ANIMAL_10': {
        'ANIMAL_NAME': 'Китайский аллигатор',
        'ANIMAL_IMAGE': 'images/china-alligator.jpg',
        'ANIMAL_KB': inline_keyboard_result_10,
        'ANIMAL_DESCRIPTION': ANIMAL_10_TEXT,
        'ANIMAL_QUALITIES': [
            'скрытность',
            'одиночка',
        ],
    },


    'ANIMAL_11': {
        'ANIMAL_NAME': 'Львиный тамарин',
        'ANIMAL_IMAGE': 'images/golden-tamarin.jpg',
        'ANIMAL_KB': inline_keyboard_result_11,
        'ANIMAL_DESCRIPTION': ANIMAL_11_TEXT,
        'ANIMAL_QUALITIES': [
            'теплолюбивость',
            'ловкость',
        ],
    },
}
