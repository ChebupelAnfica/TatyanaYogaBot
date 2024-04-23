from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пробное занятие", callback_data="trial")
        ],
        [
            InlineKeyboardButton(text="Ежемесячная подписка", callback_data="subscription_for_month")
        ],
        [
            InlineKeyboardButton(text="Доступ на месяц", callback_data="course_for_a_month")
        ],
    ],
)

trial_lesson = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Разминка", callback_data="warm_up")
        ],
        [
            InlineKeyboardButton(text="Позы стоя", callback_data="standing_positions")
        ],
        [
            InlineKeyboardButton(text="↩️️", callback_data="back_to_second_message")
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="↩️", callback_data="cancel")
        ],
    ]
)

main_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пробное занятие", callback_data="trial")
        ],
        [
            InlineKeyboardButton(text="Ежемесячная подписка", callback_data="video_subscription_for_month")
        ],
        [
            InlineKeyboardButton(text="Доступ на месяц", callback_data="video_course_for_a_month")
        ],
        [
            InlineKeyboardButton(text="Закрыть", callback_data="cancel")
        ]
    ],
)

additionally_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пробное занятие", callback_data="trial")
        ],
        [
            InlineKeyboardButton(text="Ежемесячная подписка", callback_data="subscription_for_month")
        ],
        [
            InlineKeyboardButton(text="Доступ на месяц", callback_data="course_for_a_month")
        ],
        [
            InlineKeyboardButton(text="↩️", callback_data="cancel")
        ]
    ],
)

btn_buy_month_cont = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продлить доступ на месяц (2000₽)", callback_data="btn_yoga_month")
        ]
    ]
)

btn_buy_month_auto_cont = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подключить ежемесячную подписку (2000₽)", callback_data="btn_yoga_month_auto")
        ]
    ]
)

# yoga_continue_inline_keyboard = InlineKeyboardMarkup(row_width=1)


subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ежемесячная подписка", callback_data="subscription_for_month")
        ],
        [
            InlineKeyboardButton(text="Доступ на месяц", callback_data="course_for_a_month")
        ],
        [
            InlineKeyboardButton(text="Закрыть", callback_data="cancel")
        ]
    ],
)

after_subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ежемесячная подписка", callback_data="after_subscription_for_month")
        ],
        [
            InlineKeyboardButton(text="Доступ на месяц", callback_data="after_course_for_a_month")
        ],
        [
            InlineKeyboardButton(text="Закрыть", callback_data="cancel")
        ]
    ],
)


async def btn_month(link):
    pay_button_month = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оплатить", url=link)
            ],
            [
                InlineKeyboardButton(text="↩️", callback_data="back_to_start")
            ]
        ],
    )
    return pay_button_month


async def after_btn_month(link):
    pay_button_month = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оплатить", url=link)
            ],
            [
                InlineKeyboardButton(text="↩️", callback_data="after_subscription_text")
            ]
        ],
    )
    return pay_button_month


async def video_btn_month(link):
    pay_button_month = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оплатить", url=link)
            ],
            [
                InlineKeyboardButton(text="Закрыть", callback_data="cancel")
            ]
        ],
    )
    return pay_button_month
