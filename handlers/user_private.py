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

NUM_QST = len(AMOUNT)  # максимальное количество вопросов в игре


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
                     '3 000 000, 1 500 000, 800 000, 400 000, 200 000, 100 000, 50 000, 25 000, 15 000, 10 000, 5 000, 3 000, 2 000, 1 000, 500. '
                     'Все суммы являются заменяемыми, то есть, ответив на следующий вопрос не суммируются с суммой за ответ на предыдущий.'
                     'В игре существует две несгоравмые суммы 100 000 и 5 000. '
                     'Эта сумма остаётся у игрока даже при неправильном ответе на один из последующих вопросов')


@user_private_router.callback_query(F.data.startswith('next_qst_'))
async def next_question(callback: CallbackQuery):
    st = str(callback.data)
    n = int(st.split('_')[-1])
    q = get_question(n)
    print (f'user={callback.from_user.full_name}',q)
    qst_kb = InlineKeyboardBuilder()
    for i in range(2, 6):
        qst_kb.add(InlineKeyboardButton(text=f'{i - 1}) {q[i]}', callback_data=f'qst{q[0]}_l{n}_a{i - 1}_ra{q[7]}'))
    await callback.message.answer(f'Вопрос № {n} (из {NUM_QST}):\n{q[1]}', reply_markup=qst_kb.adjust(2).as_markup())
    await callback.answer()


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
    n = int(l)
    # await callback.message.answer('<i>callback_data: ' + st + '\n lvl=' + l + ' ans=' + a + ' right_ans=' + r + '</i>')
    if a == r:
        # await callback.message.edit_reply_markup(reply_markup=)
        next_kb = InlineKeyboardBuilder()
        next_kb.add(InlineKeyboardButton(text='Следующий вопрос', callback_data=f'next_qst_{n + 1}'))
        next_kb.add(InlineKeyboardButton(text='Забрать банк!', callback_data=f'get_bank_{n}'))
        await callback.message.answer(f'<b>Верный ответ!</b>\nТвой банк: <b>{AMOUNT[n - 1]}</b>\nНесгораемая сумма: {GUARANTEED_AMOUNT[n]}',
                                      reply_markup=next_kb.adjust(2).as_markup())
    else:
        await callback.message.answer(
            f'<b>Неверный ответ!</b>\nНо ты ответил на {n - 1} вопрос(а,ов) из {NUM_QST}! Поздравляю!\nТвой выигрыш составил: <b>{GUARANTEED_AMOUNT[n - 1]}</b>')
    await callback.answer()


@user_private_router.callback_query(F.data.startswith('get_bank_'))
async def get_bank(callback: CallbackQuery):
    st = str(callback.data)[9:]
    k = int(st)
    await callback.message.answer(
        f'<b>Игра закончена!</b>\nТы ответил на {k} вопрос(а,ов) из {NUM_QST}!\nЛучше синица в руках чем журавль в небе! ;) \nТвой выигрыш: <b>{AMOUNT[k - 1]}</b>')


@user_private_router.message()
async def echo_cmd(msg: types.Message):
    await msg.answer('Вы написали: \n' + msg.text + '\n Я не понимаю вас!')
