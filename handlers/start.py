import logging

from aiogram import types, F
from aiogram.filters import Command, CommandObject


import keyboards
from data.config import ADMINS
from database import SessionLocal
from keyboards.inline.inline_keyboard_markup import main_keyboard
from loader import dp, bot
from utils.db.queries import get_user, create_user
import asyncio

@dp.message(Command("start"))
# @dp.message(CommandStart(deep_link=True))
async def cmd_start(message: types.Message,
                    command: CommandObject):
    try:
        async with SessionLocal.begin() as session:
            user = await get_user(session,
                                  message.from_user.id)
            if user is None:
                is_client = False
                await create_user(session,
                                  message.from_user.id,
                                  message.from_user.username,
                                  message.from_user.full_name)
            # session.commit()  # БОЛЬШЕ НЕ ИСПОЛЬЗУЕМ. АВТОКОММИТ РАБОТАЕТ
            else:
                is_client = user.is_yoga_access
    except Exception as ex:
        logging.error(ex)
        try:
            await bot.send_message(message.from_user.id, '''Произошла ошибка. Начните с начала -> /start''')
        except Exception as ex:
            logging.error(ex)
        return
    # if command.args:
    #     if command.args == '777':
    #         try:
    #             await bot.send_message(message.from_user.id, 'XD')
    #         except Exception as ex:
    #             logging.error(ex)
    #         return
    if is_client:
        try:
            await bot.send_message(message.from_user.id, f"""Привет, <b>{message.from_user.full_name}</b>!
Твоё меню ниже""", reply_markup=keyboards.default.personal_account.menu)
        except Exception as ex:
            logging.error(ex)
        return
    try:
        await bot.send_message(message.from_user.id, f'''Привет, <b>{message.from_user.full_name}</b>! Меня зовут Татьяна. Я преподаю йогу Айенгара в закрытом телеграмм канале tanyoga. Там есть практики в записи и в прямом эфире. Здесь вы можете оформить подписку на канал и начать заниматься вместе со мной.''')
    except Exception as ex:
        logging.error(ex)
        pass
    try:
        await asyncio.sleep(8)
    except Exception as ex:
        logging.error(ex)
        pass
    try:
        await bot.send_message(message.from_user.id, """Йога Айенгара - бережная йога. Она подходит всем - даже не гибким и людям с ограничениями по здоровью. В практике мы активно используем блоки и ремни. Так что любая асана становится доступна человеку любого уровня подготовки и растяжки.

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
🏃‍♂️Динамика""", reply_markup=main_keyboard)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.message(F.content_type.in_({'photo', 'video', 'document', 'video_note'}))
async def echo_files(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        if message.photo:
            try:
                await bot.send_message(message.from_user.id, message.photo[0].file_id)
            except:
                pass
        if message.video:
            try:
                await bot.send_message(message.from_user.id, message.video.file_id)
            except:
                pass
        if message.document:
            try:
                await bot.send_message(message.from_user.id, message.document.file_id)
            except:
                pass
        if message.video_note:
            try:
                await bot.send_message(message.from_user.id, message.video_note.file_id)
            except:
                pass
        return

