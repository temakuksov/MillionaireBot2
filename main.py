import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private_cmds

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
s = os.getenv('BOT_ADMIN')
bot_admins = [int(i) for i in s.split(',')]

dp = Dispatcher()
dp.include_router(user_private_router)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(bot_admins)
    # очистка команд бота
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_cmds, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
