from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_admin = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Mahsulotlar'), KeyboardButton(text='Add')]
    ]
)

menu_user = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Menu🧾'), KeyboardButton(text='Category🗒')]
    ]
)

menu_asosiy_admin = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Sotuvchilar'), KeyboardButton(text='Yangi Admin🆕')]
    ]
)

buyurtmani_tugatish = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Menu🧾'), KeyboardButton(text='Category🗒')],
        [KeyboardButton(text='Buyurtmani tugatish')]
    ]
)

