import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private_cmds

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()
dp.include_router(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # очистка команд бота
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_cmds,scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot,allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())