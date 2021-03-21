from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

for_what = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Практика?', callback_data='1-1')
        ],
        [
            InlineKeyboardButton(text='Лучше узнать себя?', callback_data='1-2')
        ],
        [
            InlineKeyboardButton(text='Попробовать что-то новое?', callback_data='1-3')
        ],
        [
            InlineKeyboardButton(text='Узнать, на что я способна?', callback_data='1-4')
        ],
        [
            InlineKeyboardButton(text='Разобраться в чем-то масштабном?', callback_data='1-5')
        ],
        [
            InlineKeyboardButton(text='Поиграть?', callback_data='1-6')
        ]
    ]
)