from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎟️ Подписка"),
            KeyboardButton(text="Поддержка 🫂")
        ]
    ],
    resize_keyboard=True,
)

