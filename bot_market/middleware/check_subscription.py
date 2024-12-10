from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import Bot
import logging

import loader


class CheckSubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user_id = data['event_from_user'].id
        try:
            chat_member = await self.bot.get_chat_member(chat_id=loader.CHANNEL_ID, user_id=user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                await self.bot.send_message(
                    chat_id=user_id,
                    text="Пожалуйста, подпишитесь на наш канал, чтобы продолжить работу с ботом.\n/start"
                )
                return
        except Exception as e:
            logging.error(f"Ошибка при проверке подписки: {e}")
            await self.bot.send_message(
                chat_id=user_id,
                text="Произошла ошибка при проверке подписки. Пожалуйста, попробуйте позже."
            )
            return

        return await handler(event, data)
