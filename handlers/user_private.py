import string

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import get_question

user_private_router = Router()

AMOUNT = [
    '500', '1 000', '2 000', '3 000', '5 000', '10 000',
    '15 000', '25 000', '50 000', '100 000', '200 000',
    '400 000', '800 000', '1 500 000', '3 000 000'
]  # Стоимость вопроса
GUARANTEED_AMOUNT = ['0'] * 5 + ['5 000'] * 5 + ['100 000'] * 5  # несгораемые суммы




@user_private_router.message(CommandStart())
async def start_cmd(msg: types.Message):
    start_kb = InlineKeyboardBuilder()
    start_kb.add(InlineKeyboardButton(text='Начать игру!', callback_data='next_qst_1'))
    await msg.answer(
        f'Приветствую, {msg.from_user.first_name} (id={msg.from_user.id})\nГотовы стать следующим миллионером!',
        reply_markup=start_kb.as_markup())


@user_private_router.message(Command('rules'))
async def show_rules(msg: types.Message):
    await msg.answer('<u><b>Правила игры:</b></u>\n'
                     'Для победы в игре игроку необходимо верно ответить на 15 вопросов из различных областей знаний. '
                     'Каждый вопрос имеет 4 варианта ответа, из которых только один является верным. '
                     'Сложность вопросов постоянно возрастает. Время на раздумье над каждым вопросом у игрока не ограничено. '
                     'Каждый из пятнадцати вопросов имеет конкретную денежную стоимость: '
                     '3 000 000, 1 500 000, 800 000, 400 000, 200 000, *100 000, 50 000, 25 000, 15 000, 10 000, 5 000, 3 000, 2 000, 1 000, 500.'
                     'Все суммы являются заменяемыми, то есть, ответив на следующий вопрос не суммируются с суммой за ответ на предыдущий.'
                     'В игре существует две несгоравмые суммы 100 000 и 5 000. '
                     'Эта сумма остаётся у игрока даже при неправильном ответе на один из последующих вопросов')


@user_private_router.callback_query(F.data.startswith('next_qst_'))
async def next_question(callback: CallbackQuery):
    st = str(callback.data)
    n = int(st.split('_')[-1])
    q = get_question(n)
    qst_kb = InlineKeyboardBuilder()
    for i in range(2, 6):
        qst_kb.add(InlineKeyboardButton(text=f'{i - 1}) {q[i]}', callback_data=f'qst{q[0]}_l{n}_a{i - 1}_ra{q[7]}'))
    await callback.message.answer(f'Вопрос № {n}:\n{q[1]}', reply_markup=qst_kb.adjust(2).as_markup())


@user_private_router.callback_query(F.data.startswith('qst'))
async def check_answer(callback: CallbackQuery):
    # print(callback)
    # await bot.send_message(callback.message.chat.id, callback.data)
    # await callback.answer()
    st = str(callback.data)
    a = st[st.find('a') + 1]
    r = st[-1]
    # l = string(st.split('_')[1])
    l = st[(st.find('_l') + 2):st.find('_a')]
    n = int(l) + 1
    await callback.message.answer('<i>callback_data: ' + st + '\n lvl=' + l + ' ans=' + a + ' right_ans=' + r + '</i>')
    if a == r:
        # await callback.message.edit_reply_markup(reply_markup=)
        next_kb = InlineKeyboardBuilder()
        next_kb.add(InlineKeyboardButton(text='Следующий вопрос', callback_data=f'next_qst_{n}'))
        next_kb.add(InlineKeyboardButton(text='Забрать банк!', callback_data='get_bank'))
        await callback.message.answer('<b>Верный ответ!</b>\nТвой банк: 123',
                                      reply_markup=next_kb.adjust(2).as_markup())
    else:
        await callback.message.answer('<b>Неверный ответ!</b>\nТвой выигрыш: 000')
    await callback.answer()


@user_private_router.message()
async def echo_cmd(msg: types.Message):
    await msg.answer('Вы написали: \n' + msg.text + '\n Я не понимаю вас!')
