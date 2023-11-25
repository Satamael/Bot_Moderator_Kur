import logging
import asyncio

from aiogram.types import BotCommand

from commands import bot_commands, register_user_commands
from db_scripts import init_sqlite
from bot.__init__ import bot, dp

logging.basicConfig(level=logging.DEBUG)

register_user_commands(dp)


async def main():
    init_sqlite()
    commands_bot = []
    for cmd in bot_commands.bot_commands:
        commands_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



