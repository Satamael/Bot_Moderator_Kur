from aiogram import Bot, Dispatcher

from config import API_TOKEN

__all__=['bot', 'dp']

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
