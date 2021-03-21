from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
game_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

for_what_btn = KeyboardButton(text='Зачем ты нужен?')
what_know_btn = KeyboardButton(text='Что ты обо мне знаешь?')
play_btn = KeyboardButton(text='Сыграть в игру.')

paper = KeyboardButton(text='stone')
stone = KeyboardButton(text='paper')
scissors = KeyboardButton(text='scissors')

menu.insert(for_what_btn)
menu.insert(what_know_btn)
menu.insert(play_btn)

game_kb.insert(paper)
game_kb.insert(stone)
game_kb.insert(scissors)