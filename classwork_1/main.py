from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from classwork_1.keyboard import menu, game_kb
import random

#from config import TOKEN
from states_1 import Inline_keyboard

TOKEN = '1620272486:AAFVmhtB5fFDo9mgKA8A83_kpVoKTnq96hQ'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


call_back_2 = {
    '1-1':  {'btn_text': 'Практика?', 'answer_text': 'Практики много не бывает'},
    '1-2':  {'btn_text': 'Лучше узнать себя?', 'answer_text': 'В пылком труде познаешь себя'},
    '1-3':  {'btn_text': 'Попробовать что-то новое?', 'answer_text': 'Это залог бодрости духа и ума'},
    '1-4':  {'btn_text': 'Узнать, на что я способна?', 'answer_text': 'Ещё бы)'},
    '1-5':  {'btn_text': 'Разобраться в чём-то масштабном?', 'answer_text': 'И это только начало)'},
    '1-6':  {'btn_text': 'Поиграть?', 'answer_text': 'Почему бы и нет)'},
    'last': {'btn_text': 'Ага, теперь понятно', 'answer_text': 'Поехали дальше'}
}

game = {
    'stone': {'win': 'scissors', 'draw': 'stone', 'defeat': 'paper', 'file_id': 'BQACAgIAAxkBAAICg2BTgTkB3Hoc_WYlatCFT4an9rmsAAJcDQAChFehSsOvazzqIYsNHgQ'},
    'paper': {'win': 'paper', 'draw': 'paper', 'defeat': 'scissors', 'file_id': 'BQACAgIAAxkBAAICgmBTgTmttDFoavkVBtRusiVUPT0PAAJbDQAChFehSukyRI03ojkZHgQ'},
    'scissors':{'win': 'stone', 'draw': 'scissors', 'defeat': 'scissors', 'file_id': 'BQACAgIAAxkBAAIChGBTgTk0pY8KP6voUnyrXKwFLwXhAAJdDQAChFehSiI3RiPS1vG_HgQ'}
}

#choices = ['stone', 'paper', 'scissors']

def create_kb(btn_list=[]):
    keyboard_1 = InlineKeyboardMarkup()
    buttons = list(call_back_2.keys())
    buttons.remove('last')
    if buttons == btn_list:
        keyboard_1.add(InlineKeyboardButton(text=call_back_2['last']['btn_text'], callback_data='last'))
    else:
        for call_data in buttons:
            if call_data in list(btn_list):
                continue
            else:
                keyboard_1.add(InlineKeyboardButton(text=call_back_2[call_data]['btn_text'], callback_data= call_data))
    return keyboard_1

def create_game_kb():
    keyboard = InlineKeyboardMarkup()
    buttons = list(game.keys())
    for bt in buttons:
        keyboard.add(InlineKeyboardButton(text=game[bt]['draw'], callback_data=bt))

@dp.message_handler(CommandStart())
async def hello(message: types.Message):
    if message.from_user.first_name != '' and message.from_user.last_name != '':
        await message.answer(f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.from_user.username != '':
        await message.answer(f'Здравствуйте, {message.from_user.username}!')
    else:
        await message.answer(f'Здравствуйте, {message.from_user.id}!')
    await message.answer_sticker(sticker='CAACAgIAAxkBAAL3KmBMYYtMLHIWfEOyql1umFNlGxGJAAI1AQACMNSdEbS4Nf1moLZ8HgQ',
                                 reply_markup=menu)

@dp.message_handler(lambda msg:
                    msg.text == 'Зачем ты нужен?')
async def for_what(message: types.Message):
    await message.answer('Что вас интересует?', reply_markup=create_kb())

@dp.callback_query_handler(lambda x:
                           x.data in list(call_back_2.keys()))
async def answer(call: types.CallbackQuery, state: FSMContext):
    kb = create_kb([call.data])
    await bot.edit_message_text(text=call_back_2[call.data]['answer_text'],
                                message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                reply_markup=kb)
    await Inline_keyboard.First.set()
    await state.update_data(button=[call.data])

@dp.callback_query_handler(lambda x:
                           x.data in list(call_back_2.keys()),
                           state=Inline_keyboard.First)
async def answer_2(call: types.CallbackQuery, state: FSMContext):
    buttons = await state.get_data()
    buttons = buttons.get('button')
    buttons.append(call.data)
    kb = create_kb(buttons)
    await bot.edit_message_text(
      text=call_back_2[call.data]['answer_text'],
      message_id=call.message.message_id,
      chat_id=call.message.chat.id,
      reply_markup=kb)
    await state.update_data(button=buttons)
    if call.data == 'last':
        await state.reset_state()

@dp.message_handler(lambda msg:
                    msg.text == 'Что ты обо мне знаешь?')
async def what_know_btn(message: types.Message):
    await message.answer(text=f'Ваше имя: {message.from_user.first_name} {message.from_user.last_name}\n'
                              f'Ваш никнэйм: {message.from_user.username}\n'
                              f'Ваш ID: {message.from_user.id}\n'
                              f'Язык интерфэйса: {message.from_user.language_code}\n'
                              f'Являетесь ли вы ботом: {message.from_user.is_bot}')

@dp.message_handler(lambda msg:
                    msg.text == 'Сыграть в игру.' or msg.text == 'заново')
async def start_game(message: types.Message, state: FSMContext):
    await message.answer(text='Я рада, что вы решили поиграть!\nИгра: Камень, ножницы или бумага\n'
                              'Правила:\n'
                              'Вы присылаете сообщение с текстом камень, ножницы или бумага, а я вам отправляю в ответ фото с выбором'
                              ' Игра заканчивается, когда кто-то из нас выиграет 5 раундов\n', reply_markup=game_kb)
    await Inline_keyboard.Game.set()
    await state.update_data(comp_points=0)
    await state.update_data(per_points=0)


@dp.message_handler(lambda msg:
                    msg.text in list(game.keys()),
                    state=Inline_keyboard.Game)
async def game_play(message: types.Message, state: FSMContext):
    choice = random.choice(list(game.keys()))
    await bot.send_document(chat_id=message.chat.id, document=game[choice]['file_id'], caption=choice)
    data = await state.get_data()
    comp_points = data.get('comp_points')
    per_points = data.get('per_points')
    if comp_points==5:
        await bot.send_document(chat_id=message.chat.id, document='BQACAgIAAxkBAAIEH2BU3adDb8drM0n-OTW5g91Cr1f0AAJ9DQACw7WoSpWZoyQXoK69HgQ',
                                caption='Победил компьютер. Чтобы сыграть ещё раз, напишите "заново".')
        await state.reset_state()
    if per_points==5:
        await bot.send_document(chat_id=message.chat.id, document='BQACAgIAAxkBAAIEIWBU3cImRnoXeJK-vY51NWmN0QABJQACfg0AAsO1qErAkVr7a9PbxR4E',
                                caption='Вы победили!. Чтобы сыграть ещё раз, напишите "заново".')
        await state.reset_state()
    if choice == game[choice]['win']:
        await state.update_data(comp_points=comp_points + 1)
    if choice == game[choice]['defeat']:
        await state.update_data(per_points=per_points + 1)





if __name__ == '__main__':
    executor.start_polling(dp)