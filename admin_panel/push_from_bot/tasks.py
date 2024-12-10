import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asgiref.sync import sync_to_async, async_to_sync
from celery import shared_task
from aiogram import Bot

from .models import Push
from users.models import TelegramUser

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@shared_task
def send_broadcast_message_task(push_id):
    async_to_sync(process_broadcast_message)(push_id)


async def process_broadcast_message(push_id):
    push = await sync_to_async(Push.objects.get)(id=push_id)

    users = await sync_to_async(list)(
        TelegramUser.objects.values_list('telegram_user_id', flat=True)
    )
    if await send_notify(users, push.text_message):
        push.sent = True
        await sync_to_async(push.save)()

async def send_notify(users, notify):
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=notify)
            return True
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
            return False
