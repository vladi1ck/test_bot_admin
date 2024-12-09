import logging
from doctest import debug

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import loader
from loader import bot
from utils.db_utils import Database


async def check_subscription(user_id, channel) -> bool:
    """Проверка подписки пользователя на канал"""
    try:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        logging.debug(chat_member)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as _ex:
        logging.debug(_ex)
        return False


async def check_register(user_id:int) -> bool:
    """Проверка регистрации пользователя на сервере"""
    db = Database(dsn=loader.dsn)
    try:
        await db.create_pool()
        return await db.check_user(user_id)
    except Exception as _ex:
        logging.debug(_ex)
        return False
    finally:
        await db.close_pool()


async def create_phone_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]],
            resize_keyboard=True
        )

