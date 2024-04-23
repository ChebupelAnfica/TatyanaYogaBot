import datetime
import logging

from aiogram import F, types

import keyboards.inline.close
import models
from database import SessionLocal
from loader import dp, bot
from aiogram.fsm.context import FSMContext

from utils.db.queries import get_user


@dp.message(F.text == '🎟️ Подписка')
async def bot_support(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.from_user.id, message.message_id)
    except:
        pass
    async with SessionLocal.begin() as session:
        user = await get_user(session,
                              message.from_user.id)
        if user is None:
            await bot.send_message(message.from_user.id, '❌ Не обнаружены активные подписки')
            return
        if not user.is_yoga_access:
            await bot.send_message(message.from_user.id, '❌ Не обнаружены активные подписки')
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
🎟️ Подписка на
<b>📅 Осталось дней подписки: {count_days}</b>'''

        if text_yoga_sub == '':
            await bot.send_message(message.from_user.id, '❌ Не обнаружены активные подписки')
        else:
            await bot.send_message(message.from_user.id, text_yoga_sub,
                                   reply_markup=keyboards.inline.inline_keyboard_markup.after_subscription_keyboard)


@dp.message(F.text == 'Поддержка 🫂')
async def bot_connect_with_me(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.from_user.id, message.message_id)
    except:
        pass
    try:
        await bot.send_message(message.from_user.id,
                               '''По всем интересующим вопросам и трудностям обращайтесь, пожалуйста, <a href='https://t.me/'>сюда</a>''',
                               reply_markup=keyboards.inline.close.close_inline_keyboard)
    except:
        pass
