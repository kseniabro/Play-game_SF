from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_zoo.commands.quiz_commands import CANCEL_COMMAND
from bot_zoo.texts.answer_button_text import *


# CANCEL
inline_btn_cancel = InlineKeyboardButton(
    text='Остановить опрос',
    callback_data=f'/{CANCEL_COMMAND}',
)


# QUESTION 1
inline_btn_1_1 = InlineKeyboardButton(
    text=f'{answer_1_1}',
    callback_data=f'{answer_1_1}',
)

inline_btn_1_2 = InlineKeyboardButton(
    text=f'{answer_1_2}',
    callback_data=f'{answer_1_2}',
)

inline_btn_1_3 = InlineKeyboardButton(
    text=f'{answer_1_3}',
    callback_data=f'{answer_1_3}',
)

inline_btn_1_4 = InlineKeyboardButton(
    text=f'{answer_1_4}',
    callback_data=f'{answer_1_4}',
)

inline_keyboard_1 = InlineKeyboardMarkup().\
    row(inline_btn_1_1).\
    row(inline_btn_1_2).\
    row(inline_btn_1_3).\
    row(inline_btn_1_4).\
    row(inline_btn_cancel)


# QUESTION 2
inline_btn_2_1 = InlineKeyboardButton(
    text=f'{answer_2_1}',
    callback_data=f'{answer_2_1}',
)

inline_btn_2_2 = InlineKeyboardButton(
    text=f'{answer_2_2}',
    callback_data=f'{answer_2_2}',
)

inline_btn_2_3 = InlineKeyboardButton(
    text=f'{answer_2_3}',
    callback_data=f'{answer_2_3}',
)

inline_btn_2_4 = InlineKeyboardButton(
    text=f'{answer_2_4}',
    callback_data=f'{answer_2_4}',
)

inline_keyboard_2 = InlineKeyboardMarkup().\
    row(inline_btn_2_1).\
    row(inline_btn_2_2).\
    row(inline_btn_2_3).\
    row(inline_btn_2_4).\
    row(inline_btn_cancel)


# QUESTION 3
inline_btn_3_1 = InlineKeyboardButton(
    text=f'{answer_3_1}',
    callback_data=f'{answer_3_1}',
)

inline_btn_3_2 = InlineKeyboardButton(
    text=f'{answer_3_2}',
    callback_data=f'{answer_3_2}',
)

inline_btn_3_3 = InlineKeyboardButton(
    text=f'{answer_3_3}',
    callback_data=f'{answer_3_3}',
)

inline_btn_3_4 = InlineKeyboardButton(
    text=f'{answer_3_4}',
    callback_data=f'{answer_3_4}',
)

inline_keyboard_3 = InlineKeyboardMarkup().\
    row(inline_btn_3_1).\
    row(inline_btn_3_2).\
    row(inline_btn_3_3).\
    row(inline_btn_3_4).\
    row(inline_btn_cancel)


# QUESTION 4
inline_btn_4_1 = InlineKeyboardButton(
    text=f'{answer_4_1}',
    callback_data=f'{answer_4_1}',
)

inline_btn_4_2 = InlineKeyboardButton(
    text=f'{answer_4_2}',
    callback_data=f'{answer_4_2}',
)

inline_btn_4_3 = InlineKeyboardButton(
    text=f'{answer_4_3}',
    callback_data=f'{answer_4_3}',
)

inline_btn_4_4 = InlineKeyboardButton(
    text=f'{answer_4_4}',
    callback_data=f'{answer_4_4}',
)

inline_keyboard_4 = InlineKeyboardMarkup().\
    row(inline_btn_4_1).\
    row(inline_btn_4_2).\
    row(inline_btn_4_3).\
    row(inline_btn_4_4).\
    row(inline_btn_cancel)


# QUESTION 5
inline_btn_5_1 = InlineKeyboardButton(
    text=f'{answer_5_1}',
    callback_data=f'{answer_5_1}',
)

inline_btn_5_2 = InlineKeyboardButton(
    text=f'{answer_5_2}',
    callback_data=f'{answer_5_2}',
)

inline_btn_5_3 = InlineKeyboardButton(
    text=f'{answer_5_3}',
    callback_data=f'{answer_5_3}',
)

inline_btn_5_4 = InlineKeyboardButton(
    text=f'{answer_5_4}',
    callback_data=f'{answer_5_4}',
)

inline_keyboard_5 = InlineKeyboardMarkup().\
    row(inline_btn_5_1).\
    row(inline_btn_5_2).\
    row(inline_btn_5_3).\
    row(inline_btn_5_4).\
    row(inline_btn_cancel)
