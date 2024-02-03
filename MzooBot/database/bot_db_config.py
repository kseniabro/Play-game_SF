import logging
import sqlite3 as sql

from datetime import datetime
from aiogram.dispatcher.storage import FSMContext

connect = sql.connect(r'database/zoo_bot_database.db')
curs = connect.cursor()


async def db_start():
    """Функция, создающая таблицу в базе данных для учёта ответов пользователей.
    Если таблица уже существует, то просто подключается к ней."""

    if connect:
        logging.info(f' {datetime.now()} : Successfully connected to database.')

    curs.execute(
        """CREATE TABLE IF NOT EXISTS quiz_results (
        user_id TEXT PRIMARY KEY,
        answers TEXT)"""
    )
    connect.commit()


async def db_insert_new_results(state: FSMContext):
    """Функция для вставки новой записи с результатами опроса,
    если пользователь впервые его проходит."""

    async with state.proxy() as data:
        user = str(data.get('user_id'))
        user_results = data.get('1st_question') + ", " \
            + data.get('2nd_question') + ", " \
            + data.get('3rd_question') + ", " \
            + data.get('4th_question') + ", " \
            + data.get('5th_question')

        to_insert = (user, user_results)
        curs.execute(
            """INSERT INTO quiz_results
            VALUES (?, ?)""",
            to_insert,
        )
        connect.commit()
        logging.info(f' {datetime.now()} : New record successfully added to database.')


async def db_delete_old_results(state: FSMContext):
    """Функция, удаляющая существующую запись с результатами опроса,
    если пользователь его уже проходил."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        curs.execute(f"""DELETE FROM quiz_results WHERE user_id = '{user_id}'""")
        connect.commit()
        logging.info(f' {datetime.now()} : Old record successfully deleted from database.')
        await db_insert_new_results(state=state)


async def check_user_db_record(state: FSMContext):
    """Функция для проверки проходил ли уже текущий пользователь опрос хотя бы один раз."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        find = curs.execute(f"""SELECT user_id FROM quiz_results WHERE user_id = '{user_id}'""")

        if not find:
            await db_insert_new_results(state=state)
        else:
            await db_delete_old_results(state=state)
