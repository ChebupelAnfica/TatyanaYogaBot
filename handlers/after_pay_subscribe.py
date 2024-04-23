from aiogram import types, F
import uuid
import datetime
import keyboards
from database import SessionLocal
from loader import dp, bot
import logging
import requests
from utils.db.queries import get_user
from aiogram.fsm.context import FSMContext


@dp.callback_query(F.data == 'after_subscription_for_month')
async def subscription(call: types.CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, call.from_user.id)
        if user is None:
            await bot.send_message(call.from_user.id, 'Произошла ошибка, нажмите /start и повторите процедуру')
            return
    order_id = f'{call.from_user.id}:{uuid.uuid4()}:m'
    link_url = f'https://tanyoga.payform.ru/?do=link&products%5B0%5D%5Bname%5D=Доступ+к+каналу+Йога+Айенгара+на+месяц&products%5B0%5D%5Bprice%5D=5000&products%5B0%5D%5Bquantity%5D=1&order_id={order_id}&subscription=1755504&paid_content=https%3A%2F%2Ft.me%2F%2BExJqlYrejBxmMmQx'
    link = requests.get(link_url).text
    await bot.edit_message_text('''Доступ на месяц стоит 5000 рублей.

Платеж списывается автоматически ежемесячно.

ℹ Чтобы оплатить доступ, воспользуйтесь кнопкой ниже.
ℹ Платеж обрабатывается автоматически''',
                                call.from_user.id, call.message.message_id,
                                reply_markup=await keyboards.inline.inline_keyboard_markup.after_btn_month(link))
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.callback_query(F.data == 'after_course_for_a_month')
async def course_for_month(call: types.CallbackQuery, state: FSMContext):
    async with SessionLocal() as session:
        user = await get_user(session, call.from_user.id)
        if user is None:
            await bot.send_message(call.from_user.id, 'Произошла ошибка, нажмите /start и повторите процедуру')
            return
    order_id = f'{call.from_user.id}:{uuid.uuid4()}:m'
    link_url = f'https://tanyoga.payform.ru/?do=link&products%5B0%5D%5Bname%5D=Доступ+к+каналу+Йога+Айенгара+на+месяц&products%5B0%5D%5Bprice%5D=5000&products%5B0%5D%5Bquantity%5D=1&order_id={order_id}&paid_content=https%3A%2F%2Ft.me%2F%2BExJqlYrejBxmMmQx'
    link = requests.get(link_url).text
    await bot.edit_message_text('''Доступ на месяц стоит 5000 рублей.

ℹ Чтобы оплатить доступ, воспользуйтесь кнопкой ниже.
ℹ Платеж обрабатывается автоматически''',
                                call.from_user.id, call.message.message_id,
                                reply_markup=await keyboards.inline.inline_keyboard_markup.after_btn_month(link))
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.callback_query(F.data == 'after_subscription_text')
async def bot_support(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except:
        pass
    async with SessionLocal.begin() as session:
        user = await get_user(session,
                              callback_query.from_user.id)
        if user is None:
            await bot.send_message(callback_query.from_user.id, '❌ Не обнаружены активные подписки')
            return
        if not user.is_yoga_access:
            await bot.send_message(callback_query.from_user.id, '❌ Не обнаружены активные подписки')
            return
        text_yoga_sub = ''
        if user.is_yoga_access:
            try:
                delta_date = user.date_end_yoga - datetime.datetime.now().date()
            except:
                pass
            if ',' not in str(delta_date):
                count_days = '0'
            else:
                list_date = str(delta_date).split(',')
                count_days = list_date[0].split(' ')[0].strip()
                if '-' in count_days:
                    user.is_yoga_access = False
                    user.date_end_yoga = None
                    session.commit()

            text_yoga_sub = f'''
🎟 Подписка на
<b>📅 Осталось дней подписки: {count_days}</b>'''

        if text_yoga_sub == '':
            await bot.send_message(callback_query.from_user.id, '❌ Не обнаружены активные подписки')
        else:
            await bot.send_message(callback_query.from_user.id, text_yoga_sub,
                                   reply_markup=keyboards.inline.inline_keyboard_markup.after_subscription_keyboard)
