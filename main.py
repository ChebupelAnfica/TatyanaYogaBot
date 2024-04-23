import asyncio
import datetime
import logging
from urllib.parse import unquote

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import keyboards
import models
from data.config import ADMINS, YOGA_CHANNEL
from database import SessionLocal
from loader import bot
from utils.db.queries import get_user_phone, get_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/notify')
async def get_notify(request: Request):
    """Центр уведомлений"""
    data = await request.body()
    check = str(data)

    if '&payment_status=success' in check:
        date = '~'
        sum = '0.00'
        order_id = '0'
        phone = '~'
        order_id_normal = '0'
        payment_type = '~'
        payment_status = 'No'
        payment_init = '~'
        maybe_autosub = '~'
        subscription_date_next_payment = '~'

        transaction_list = check.split('&')
        for elem in transaction_list:
            if 'date=' in elem:
                date = datetime.datetime.strptime(elem.split('=')[1][:10], "%Y-%m-%d").date()
            if 'order_num' in elem:
                order_id = elem.split('=')[1]
            if 'order_id' in elem:
                order_id_normal = elem.split('=')[1]
            if 'sum=' in elem:
                sum = transaction_list[4].split('=')[1]
            if 'customer_phone=' in elem:
                phone = unquote(elem.split('=')[1])
            if 'payment_type=' in elem:
                payment_type = unquote(elem.split('=')[1])
            if 'payment_init=' in elem:
                payment_init = elem.split('=')[1]
            if 'subscription' in elem:
                maybe_autosub = 'yes'
            if payment_type == 'Автоплатеж' and order_id_normal != '0':
                subscription_date_next_payment = date + datetime.timedelta(days=31)

        async with SessionLocal() as session:
            full_info = str(date) + ' ' + sum + ' ' + phone + ' ' + payment_type + ' ' + payment_status + ' ' + \
                        payment_init + ' ' + str(subscription_date_next_payment) + ' ' + maybe_autosub
            try:
                try:
                    user_id_from_order = int(order_id.split('%3A')[0])
                except Exception as ex:
                    logging.error(ex)
                    async with SessionLocal() as session:
                        try:
                            phone_user = await get_user_phone(session, phone)
                            if not phone_user:
                                raise
                        except Exception as ex:
                            logging.error(ex)
                            raise
                        else:
                            user_id_from_order = phone_user.id_user
            except Exception as ex:
                for admin_id in ADMINS:
                    await bot.send_message(admin_id, f'{ex}')
                    return
            sub_type = order_id.split('%3A')[2]
            user = await get_user(session, user_id_from_order)
            if payment_type == 'Автоплатеж' or (payment_init == "manual" or payment_init == "manual'"):
                if sub_type == 'm':
                    if user.date_end_yoga is None:
                        user.date_end_yoga = datetime.date.today()
                user_is_yoga_access = user.is_yoga_access
                if sub_type == 'm':
                    if payment_type == 'Автоплатеж':
                        if user.date_end_yoga != subscription_date_next_payment:
                            user.date_end_yoga = subscription_date_next_payment
                            user.is_yoga_access = True
                    else:
                        if user.is_yoga_access:
                            date_start = user.date_end_yoga
                        else:
                            date_start = datetime.date.today()
                        if user.date_end_yoga != date_start + datetime.timedelta(days=30):
                            user.date_end_yoga = date_start + datetime.timedelta(days=30)
                            user.is_yoga_access = True

                user.is_last_client = True
                user.phone = phone
                user.is_subscriber = False if full_info.split(' ')[-1] == '~' else True
                session.commit()

                if sub_type == 'm':
                    if not user_is_yoga_access:
                        try:
                            await bot.ban_chat_member(YOGA_CHANNEL, user.id_user)
                        except Exception as ex:
                            logging.error(ex)
                            for admin in ADMINS:
                                try:
                                    await bot.send_message(admin, f'''[ВНИМАНИЕ]
Клиент: {phone}
ID: {user_id_from_order}
Процесс: Бан в канале
Ошибка: ❌ Не смог забанить
Человек оплатил''', reply_markup=keyboards.inline.close.close_inline_keyboard)
                                except Exception as ex:
                                    logging.error(ex)
                                    pass
                        await asyncio.sleep(1)
                        try:
                            await bot.unban_chat_member(YOGA_CHANNEL, user.id_user)
                        except Exception as ex:
                            logging.error(ex)
                            for admin in ADMINS:
                                try:
                                    await bot.send_message(admin, f'''[ВНИМАНИЕ]
Клиент: {phone}
ID: {user_id_from_order}
Процесс: Разбан в канале
Ошибка: ❌ Не смог разбанить
Человек оплатил''',
                                                           reply_markup=keyboards.inline.close.close_inline_keyboard)
                                except Exception as ex:
                                    logging.error(ex)
                                    pass
                        # invite_link_private_channel = await bot.create_chat_invite_link(
                        #     chat_id=YOGA_CHANNEL,
                        #     member_limit=1)
                        await bot.send_message(user.id_user, f'''
<b>✅Платеж получен

Ваш доступ к группе:
🔗 https://t.me/+ExJqlYrejBxmMmQx</b>
''', parse_mode='HTML', reply_markup=keyboards.default.personal_account.menu)

                    else:
                        await bot.send_message(user.id_user, f'''
<b>✅ Платеж получен. Доступ к каналу продлен</b>
''', parse_mode='HTML', reply_markup=keyboards.default.personal_account.menu)

    return {'answer': 'yes'}
