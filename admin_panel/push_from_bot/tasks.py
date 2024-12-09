import asyncio
import json
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from celery import shared_task
from aiogram import Bot, types
from django.conf import settings
from .models import Push
from users.models import TelegramUser  # Модель пользователей с telegram_id

bot = Bot(token=os.getenv('BOT_TOKEN'),default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@shared_task
def send_broadcast_message(push_id):
    # Используем asyncio.run() для запуска асинхронных задач
    asyncio.run(send_broadcast_message(push_id))

@shared_task
async def send_broadcast_message(push_id):
    push = Push.objects.get(id=push_id)
    users = TelegramUser.objects.values_list('telegram_user_id', flat=True)

    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=json.dumps(push.message))
        except Exception as e:
            # Логирование ошибки
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    # Обновляем статус рассылки
    push.sent = True
    push.save()