from aiogram import F, types

from loader import dp, bot
from keyboards.inline.inline_keyboard_markup import trial_lesson, main_back_keyboard, main_keyboard
import logging
from aiogram.fsm.context import FSMContext

video_id1 = "BAACAgIAAxkBAAMjZfCANRuR0SQf0G3KVCJkoUWyb8kAAtZGAAIQo4FLUKowgRZoIAs0BA"
video_id2 = "BAACAgIAAxkBAAM0ZfCReU8n1dmlT7iCBTAtUV0JKRgAAotFAAIQo4lLHRzGMpZG6zc0BA"


@dp.callback_query(lambda call: call.data == 'trial')
async def process_callback1(call: types.CallbackQuery):
    try:
        await bot.edit_message_text(f'''На канале подробно разбираю каждую асану, как ее выполнять, технику безопасности и ограничения по здоровью.
Также на канале будет 20-недельный курс для начинающих и асаны от 75 различных заболеваний и проблем по здоровью.
 
Всему можно научиться практикуя на канале и задавая вопросы, даже если вы до этого никогда не занимались раньше йогой.

Если у вас возникает вопрос по технике выполнения, можно прислать фото асан в комментарии под любой практикой или просто описать свои ощущения. Я на все вопросы отвечаю.''',
                                    call.from_user.id, call.message.message_id,
                                    reply_markup=trial_lesson)
    except Exception as ex:
        logging.error(ex)
        pass
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)


@dp.callback_query(lambda call: call.data == 'warm_up')
async def process_callback2(call: types.CallbackQuery):
    try:
        await bot.send_video(call.from_user.id, video_id1,
                             caption="Здесь представлены упражнения, которые помогут вам в дальнейшем постижении нашего курса.",
                             reply_markup=main_back_keyboard)
    except Exception as ex:
        logging.error(ex)
        pass
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)


@dp.callback_query(lambda call: call.data == 'standing_positions')
async def process_callback3(call: types.CallbackQuery):
    try:
        await bot.send_video(call.from_user.id, video_id2,
                             caption="Здесь представлены упражнения, которые можно выполнять, стоя.",
                             reply_markup=main_back_keyboard)
    except Exception as ex:
        logging.error(ex)
        pass
    try:
        await bot.answer_callback_query(call.id)
    except Exception as ex:
        logging.error(ex)


@dp.callback_query(F.data == 'back_to_second_message')
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