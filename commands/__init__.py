__all__ = ['bot_commands']

from aiogram import  filters
from aiogram import  Router
from use_commands import cmd_start, mute, ban, report, rasban, list_ban, list_mute, rasmute, cmd_help


def register_user_commands(router: Router) -> None:
    router.message.register(cmd_start, filters.Command(commands=['start']))
    router.message.register(cmd_help, filters.Command(commands=['help']))
    router.message.register(mute, filters.Command(commands=['mute']))
    router.message.register(ban, filters.Command(commands=['ban']))
    router.message.register(report, filters.Command(commands=['report']))
    router.message.register(rasban, filters.Command(commands=['unban']))
    router.message.register(list_ban, filters.Command(commands=['ban_users']))
    router.message.register(list_mute, filters.Command(commands=['mute_users']))
    router.message.register(rasmute, filters.Command(commands=['unmute']))
