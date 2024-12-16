from aiogram import Bot, types, Router
from aiogram.filters import CommandStart, Command

from database.crud import get_question

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(msg: types.Message):
    await msg.answer(f'Приветствую, {msg.from_user.first_name} (id={msg.from_user.id})')


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


@user_private_router.message()
async def echo_cmd(msg: types.Message):
    await msg.answer('Вы написали: \n' + msg.text + '\n я не понимаю!')
