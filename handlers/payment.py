from aiogram import types, F
import uuid

import keyboards
from database import SessionLocal
from loader import dp, bot
from keyboards.inline.inline_keyboard_markup import main_keyboard
import logging
import requests
from utils.db.queries import get_user
from aiogram.fsm.context import FSMContext


@dp.callback_query(F.data == 'subscription_for_month')
async def subscription(call: types.CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, call.from_user.id)
        if user is None:
            await bot.send_message(call.from_user.id, 'Произошла ошибка, нажмите /start и повторите процедуру')
            return
    order_id = f'{call.from_user.id}:{uuid.uuid4()}:m'
    link_url = f'Cсылка'
    link = requests.get(link_url).text
    await bot.edit_message_text(f'''Доступ на месяц стоит 5000 рублей.

Платеж списывается автоматически ежемесячно.

ℹ Чтобы оплатить доступ, воспользуйтесь кнопкой ниже.
ℹ Платеж обрабатывается автоматически''',
                                call.from_user.id, call.message.message_id,
                                reply_markup=await keyboards.inline.inline_keyboard_markup.btn_month(link))
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.callback_query(F.data == 'course_for_a_month')
async def course_for_month(call: types.CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, call.from_user.id)
        if user is None:
            await bot.send_message(call.from_user.id, 'Произошла ошибка, нажмите /start и повторите процедуру')
            return
    order_id = f'{call.from_user.id}:{uuid.uuid4()}:m'
    link_url = f'Ссылка'
    link = requests.get(link_url).text
    await bot.edit_message_text(f'''Доступ на месяц стоит 5000 рублей.
    
ℹ Чтобы оплатить доступ, воспользуйтесь кнопкой ниже.
ℹ Платеж обрабатывается автоматически''',
                                call.from_user.id, call.message.message_id,
                                reply_markup=await keyboards.inline.inline_keyboard_markup.btn_month(link))
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.callback_query(F.data == 'back_to_start')
async def process_back(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)
        pass
    try:
        await bot.edit_message_text("""Йога Айенгара - бережная йога. Она подходит всем - даже не гибким и людям с ограничениями по здоровью. В практике мы активно используем блоки и ремни. Так что любая асана становится доступна человеку любого уровня подготовки и растяжки.

Регулярные занятия позволят улучшить здоровье, укрепить тело, развить гибкисть, снять стресс, успокоить эмоции и ум, почувствовать спокойствие и умиротворение, ощутить расслабленное тело в конце каждой практики.

Практики на канале идут от простого к сложному. Подходят для начального уровня и продвинутого. Сначала мы знакомимся со всеми асанами. Для удобства я разделила их на 9 групп:

🧍🏼‍♀️Позы стоя
🧘‍♀️Позы сидя
💆🏼‍♀️Позы лежа
🧎‍♀️Скрутки
🤾Прогибы
🚶🏼‍♂️Баланс и раскрытие таза
🙇🏼‍♀️Наклоны вперед
🤸‍♂️Перевернутые асаны
🏃‍♂️Динамика""",
                                    call.from_user.id,
                                    call.message.message_id,
                                    reply_markup=main_keyboard)
    except Exception as ex:
        logging.error(ex)


@dp.callback_query(lambda c: c.data == 'video_subscription_for_month')
async def video_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, callback_query.from_user.id)
        if user is None:
            await bot.send_message(callback_query.from_user.id,
                                   'Произошла ошибка, нажмите /start и повторите процедуру')
            return

    order_id = f'{callback_query.from_user.id}:{uuid.uuid4()}:m'
    link_url = f''
    link = requests.get(link_url).text

    await bot.send_message(callback_query.from_user.id,
                           f'''Доступ на месяц стоит 5000 рублей.

Платеж списывается автоматически ежемесячно.

ℹ️ Чтобы оплатить доступ, воспользуйтесь кнопкой ниже.
ℹ️ Платеж обрабатывается автоматически''',
                           reply_markup=await keyboards.inline.inline_keyboard_markup.video_btn_month(link))
    try:
        await bot.answer_callback_query(callback_query.id)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.callback_query(lambda c: c.data == 'video_course_for_a_month')
async def video_course_for_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, callback_query.from_user.id)
        if user is None:
            await bot.send_message(callback_query.from_user.id,
                                   'Произошла ошибка, нажмите /start и повторите процедуру')
            return

    order_id = f'{callback_query.from_user.id}:{uuid.uuid4()}:m'
    link_url = f''
    link = requests.get(link_url).text

    await bot.send_message(callback_query.from_user.id,
                           f'''Доступ на месяц стоит 5000 рублей.

ℹ️ Чтобы оплатить доступ, воспользуйтесь кнопкой ниже.
ℹ️ Платеж обрабатывается автоматически''',
                           reply_markup=await keyboards.inline.inline_keyboard_markup.video_btn_month(link))
    try:
        await bot.answer_callback_query(callback_query.id)
    except Exception as ex:
        logging.error(ex)
        pass
