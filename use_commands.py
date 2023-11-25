import traceback
from datetime import datetime, timedelta

from aiogram import types, Bot
from aiogram.types import Message
from config import ADMIN
import bot.__init__ as m
from db_scripts import insertToMute, insertToBan, getUser, select_ban_user, select_mute_user


async def cmd_start(message: Message):
    await message.reply("Привет!\nЯ ваш администратор!")


async def cmd_help(message: Message):
    str = "Мои возможности:\r\n"
    str += ("Для админа:\r\n"
            "mute - Замьютить пользователя на сутки,\r\n"
            "ban - Бан пользователя,\r\n"
            "unban - Разбанить пользователя,\r\n"
            "unmute - Размьютить пользователя,\r\n"
            "ban_users - Забаненные пользователи,\r\n"
            "mute_users - Замьюченные пользователи\r\n"
            "Для пользователя:\r\n"
            "start - Начать,\r\n"
            "help - Помощь,\r\n"
            "report - Предупреждение админа\r\n")
    await message.reply(str)

async def ban(message: Message):
    users = await m.bot.get_chat_administrators(chat_id=message.chat.id)
    admins = [user.user.id for user in users]
    if message.from_user.id in admins:
        try:
            user_id = message.reply_to_message.from_user.id

            insertToBan(user_id, message.reply_to_message.from_user.full_name,
                        datetime.now(), True, message.text)

            await m.bot.ban_chat_member(message.chat.id, user_id)
            await message.answer(f'Пользователь {user_id} был забанен')
        except:
            await message.answer('Что-то пошло не так')
    else:
        await message.answer("Вы не являетесь администратором")


async def mute(message: Message):
    users = await m.bot.get_chat_administrators(chat_id=message.chat.id)
    admins = [user.user.id for user in users]
    if message.from_user.id in admins:
        user_id = message.reply_to_message.from_user.id
        dt = datetime.now() + timedelta(days=1)
        timestamp = dt.timestamp()
        cause = message.text
        insertToMute(user_id, message.reply_to_message.from_user.full_name, dt, cause)
        try:
            await m.bot.restrict_chat_member(message.chat.id, user_id,
                                       types.ChatPermissions(can_send_messages = False), until_date=timestamp)
            await message.answer('Пользователь успешно замьютен')
        except Exception as e:
            await message.answer(traceback.format_exc())
    else:
        await message.answer("Вы не являетесь администратором")



async def rasban(message: Message):
    users = await m.bot.get_chat_administrators(chat_id=message.chat.id)
    admins = [user.user.id for user in users]
    if message.from_user.id in admins:
        user_id = message.reply_to_message.from_user.id
        await m.bot.unban_chat_member(user_id = user_id, chat_id=message.chat.id, only_if_banned = True)
        insertToBan(user_id, message.reply_to_message.from_user.full_name,
                    "", False, "")
        await message.answer("Пользователь был разбанен")
    else:
        await message.answer("Вы не являетесь администратором")

async def rasmute(message: Message):
    users = await m.bot.get_chat_administrators(chat_id=message.chat.id)
    admins = [user.user.id for user in users]
    if message.from_user.id in admins:
        user_id = message.reply_to_message.from_user.id
        await m.bot.restrict_chat_member(message.chat.id, user_id,
                                         types.ChatPermissions(can_send_messages=True))
        insertToMute(user_id, message.reply_to_message.from_user.full_name,
                    None,  "")
        await message.answer("Пользователь был размьючен")
    else:
        await message.answer("Вы не являетесь администратором")
async def report(message: Message):
    await m.bot.forward_message(
        chat_id=ADMIN,
        from_chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id)

async def list_ban(message: Message):
    users = await m.bot.get_chat_administrators(chat_id=message.chat.id)
    admins = [user.user.id for user in users]
    if message.from_user.id in admins:
        users = select_ban_user()
        str = "Забаненные пользователи:\r\n Ник Причина Количество раз\r\n"
        if len(users) != 0:
            str += '\r\n'.join(users)
            await message.answer(str)
        else:
            await message.answer("Нет таких")
    else:
        await message.answer("Вы не являетесь администратором")


async def list_mute(message: Message):
    users = await m.bot.get_chat_administrators(chat_id=message.chat.id)
    admins = [user.user.id for user in users]
    if message.from_user.id in admins:
        users = select_mute_user()
        str = "Замьченные пользователи:\r\n"
        if len(users) != 0:
            str += '\r\n'.join(users)
            print(str)
            await message.answer(str)
        else:
            await message.answer("Нет таких")
    else:
        await message.answer("Вы не являетесь администратором")
