from aiogram.types import BotCommand

private_cmds = [
    BotCommand(command='start', description='Начать игру!'),
    BotCommand(command='rules', description='Посмотреть правила игры'),
    BotCommand(command='top10', description='Топ 10 игроков')
]
