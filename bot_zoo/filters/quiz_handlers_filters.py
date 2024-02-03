from aiogram import types


async def cancel_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'cancel':
        return callback_query


async def question_filter_1(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_2(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_3(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_4(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_5(callback_query: types.CallbackQuery):
    return callback_query