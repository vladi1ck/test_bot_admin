from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import Bot
import logging

import loader
from utils.utils import check_register


class CheckRegistrationMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user_id = data['event_from_user'].id
        try:
            if not await check_register(user_id):
                await self.bot.send_message(
                    chat_id=user_id,
                    text="Пожалуйста, пройди регистрацию, чтобы продолжить работу с ботом.\n/register"
                )
                return
        except Exception as e:
            logging.error(f"Ошибка при проверке подписки: {e}")
            await self.bot.send_message(
                chat_id=user_id,
                text="Произошла ошибка при проверке регистрации. Пожалуйста, попробуйте позже."
            )
            return

        return await handler(event, data)
