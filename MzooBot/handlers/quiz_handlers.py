import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_zoo.bot_settings2 import bot
from bot_zoo.commands.quiz_commands import START_QUIZ_COMMAND, CANCEL_COMMAND
from bot_zoo.filters.result_filters import get_totem_animal
from bot_zoo.texts.answer_button_text import *
from bot_zoo.database.bot_db_config import check_user_db_record, db_start

from bot_zoo.filters.quiz_handlers_filters import (
    cancel_inline_btn_filter,
    question_filter_1,
    question_filter_2,
    question_filter_3,
    question_filter_4,
    question_filter_5,
)

from bot_zoo.texts.warnings_text import (
    NOT_NONE_STATE_CANCEL_COMMAND_TEXT,
    NONE_STATE_CANCEL_COMMAND_TEXT,
    ALREADY_ANSWERED,
    ALREADY_FINISHED,
)

from bot_zoo.texts.questions_text import (
    START_QUIZ_TEXT,
    QUESTION_1,
    QUESTION_2,
    QUESTION_3,
    QUESTION_4,
    QUESTION_5,
    END_MESSAGE,
)

from bot_zoo.keyboards.quiz_kb import (
    inline_keyboard_1,
    inline_keyboard_2,
    inline_keyboard_3,
    inline_keyboard_4,
    inline_keyboard_5,
)


# Quiz handlers
class CurrentQuestion(StatesGroup):
    """Класс для фиксации состояний ожидания ответа на определённый по счёту вопрос."""

    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel, введённой вручную. Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to cancel empty state.')
        await message.answer(text=NONE_STATE_CANCEL_COMMAND_TEXT)
        return

    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} cancelled '
                 f'quiz at {current_state} state by command.')
    await state.reset_state()
    await message.answer(text=NOT_NONE_STATE_CANCEL_COMMAND_TEXT)


async def cancel_inline_button(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel, вызванная через инлайн-кнопку. Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} tried to cancel empty state.')
        await callback.answer()
        await callback.message.answer(text=NONE_STATE_CANCEL_COMMAND_TEXT)
        return

    logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} cancelled '
                 f'quiz at {current_state} state by inline button.')
    await state.reset_state()
    await callback.answer()
    await callback.message.answer(text=NOT_NONE_STATE_CANCEL_COMMAND_TEXT)


async def animal_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды запуска опроса."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} started new quiz.')
    else:
        await message.answer(text='Вы начали опрос заново.')
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} restarted quiz.')

    await message.answer(text=START_QUIZ_TEXT)
    await message.answer_photo(
        photo=open('images/EWFW.jpg', 'br'),
        caption=QUESTION_1,
        reply_markup=inline_keyboard_1
    )
    await CurrentQuestion.question_1.set()


async def process_question_1(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_1_1}'
            or callback_query.data == f'{answer_1_2}'
            or callback_query.data == f'{answer_1_3}'
            or callback_query.data == f'{answer_1_4}'):

        if cur_state == 'CurrentQuestion:question_1':
            await bot.answer_callback_query(callback_query.id)
            await db_start()
            async with state.proxy() as data:
                data['user_id'] = callback_query.from_user.id
                data['1st_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 1st question.')
            await CurrentQuestion.next()
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=open('images/food.jpg', 'br'),
                caption=QUESTION_2,
                reply_markup=inline_keyboard_2,
            )

        elif cur_state != 'CurrentQuestion:question_1' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 1st question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 1st question again in already finished quiz.')

    else:
        await process_question_2(callback_query=callback_query, state=state)


async def process_question_2(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_2_1}'
            or callback_query.data == f'{answer_2_2}'
            or callback_query.data == f'{answer_2_3}'
            or callback_query.data == f'{answer_2_4}'):

        if cur_state == 'CurrentQuestion:question_2':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['2nd_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 2nd question.')
            await CurrentQuestion.next()
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=open('images/time_of_day.jpg', 'br'),
                caption=QUESTION_3,
                reply_markup=inline_keyboard_3,
            )

        elif cur_state != 'CurrentQuestion:question_2' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 2nd question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 2nd question again in already finished quiz.')

    else:
        await process_question_3(callback_query=callback_query, state=state)


async def process_question_3(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_3_1}'
            or callback_query.data == f'{answer_3_2}'
            or callback_query.data == f'{answer_3_3}'
            or callback_query.data == f'{answer_3_4}'):

        if cur_state == 'CurrentQuestion:question_3':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['3rd_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 3rd question.')
            await CurrentQuestion.next()
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=open('images/moods.jpg', 'br'),
                caption=QUESTION_4,
                reply_markup=inline_keyboard_4,
            )

        elif cur_state != 'CurrentQuestion:question_3' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 3rd question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 3rd question again in already finished quiz.')

    else:
        await process_question_4(callback_query=callback_query, state=state)


async def process_question_4(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_4_1}'
            or callback_query.data == f'{answer_4_2}'
            or callback_query.data == f'{answer_4_3}'
            or callback_query.data == f'{answer_4_4}'):

        if cur_state == 'CurrentQuestion:question_4':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['4th_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 4th question.')
            await CurrentQuestion.next()
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=open('images/weather.jpg', 'br'),
                caption=QUESTION_5,
                reply_markup=inline_keyboard_5,
            )

        elif cur_state != 'CurrentQuestion:question_4' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 4th question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 4th question again in already finished quiz.')

    else:
        await process_question_5(callback_query=callback_query, state=state)


async def process_question_5(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_5_1}'
        or callback_query.data == f'{answer_5_2}'
        or callback_query.data == f'{answer_5_3}'
        or callback_query.data == f'{answer_5_4}')\
            and cur_state == 'CurrentQuestion:question_5':
        await bot.answer_callback_query(callback_query.id)
        async with state.proxy() as data:
            data['5th_question'] = callback_query.data
            proxy_dict = data.as_dict()
            result = await get_totem_animal(proxy_dict=proxy_dict)
        await check_user_db_record(state=state)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 5th question.')
        await state.finish()
        await bot.send_photo(
            chat_id=result.get('chat_id'),
            photo=open(f"{result.get('photo')}", 'br'),
            caption=result.get('caption'),
            reply_markup=result.get('reply_markup'),
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=END_MESSAGE,
        )

    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_FINISHED}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 5th question again in already finished quiz.')


# ---------------------
# Handlers registration
def register_quiz_handlers(disp: Dispatcher):
    disp.register_message_handler(
        cancel_command,
        commands=[f'{CANCEL_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        cancel_inline_button,
        cancel_inline_btn_filter,
        state='*',
    )
    disp.register_message_handler(
        animal_command,
        commands=[f'{START_QUIZ_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_1,
        question_filter_1,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_2,
        question_filter_2,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_3,
        question_filter_3,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_4,
        question_filter_4,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_5,
        question_filter_5,
        state='*',
    )