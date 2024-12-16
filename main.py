import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private_cmds
from database.crud import get_question

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
s = os.getenv('BOT_ADMIN')
bot_admins = [int(i) for i in s.split(',')]

dp = Dispatcher()
dp.include_router(user_private_router)


@dp.message(Command('next'))
async def next_question(msg: types.Message):
    q = get_question(1)
    question_kb = InlineKeyboardBuilder()
    for i in range(2, 6):
        question_kb.add(InlineKeyboardButton(text=f'{i - 1}) {q[i]}', callback_data=f'qst_{q[0]}_ans_{q[i]}'))
    await msg.answer(f'Вопрос 1:\n{q[1]}', reply_markup=question_kb.adjust(2).as_markup())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # очистка команд бота
    print(bot_admins)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_cmds, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
