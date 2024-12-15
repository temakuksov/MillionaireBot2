import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(msg: types.Message):
    await msg.answer(f'Приветствую, {msg.from_user.first_name}!\nГотовы стать следующим миллионером?')


@dp.message()
async def echo_cmd(msg: types.Message):
    await msg.answer('Вы написали: \n'+msg.text+'\n я не понимаю!')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())