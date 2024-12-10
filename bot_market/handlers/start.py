import logging
import os

import dotenv
from aiogram import Router, types
from aiogram.filters import  CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.registration import registration
from keyboards.main_keyboards import main_kb
from states.register import Registration
from utils.utils import check_subscription, check_register

dotenv.load_dotenv()
start_router = Router()
CHANNEL_ID = os.getenv('CHANNEL_ID')


@start_router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id, channel=CHANNEL_ID)
    is_register = await check_register(user_id)


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подписаться на канал", url=f"https://t.me/{CHANNEL_ID}")],
            [InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription")]
        ]
    )

    if is_subscribed and is_register:
        await message.answer("Добро пожаловать! ", reply_markup=await main_kb())
    elif is_register:
        await message.answer("Для продолжения подпишитесь на наш канал.", reply_markup=keyboard)
    elif is_subscribed:
        await registration(message, state)
    else:
        # keyboard = keyboard.inline_keyboard.append([InlineKeyboardButton(text="Регистрация")])
        await message.answer('Для продолжения необходимо зарегистрироваться и подписаться на канал', reply_markup=keyboard)


@start_router.callback_query(lambda call: call.data == "check_subscription")
async def callback_check_subscription(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    is_subscribed = await check_subscription(user_id, channel=CHANNEL_ID)
    is_register = await check_register(user_id)

    if is_subscribed:
        await call.message.edit_text("Спасибо за подписку! Теперь вы можете продолжить.")
        if is_register:
            await call.message.answer('Добро пожаловать!', reply_markup=await main_kb())
        else:
            await call.message.answer('Регистрация')
            await call.message.answer("Введите ваше имя:")
            await state.set_state(Registration.first_name)

    else:
        await call.answer("Вы ещё не подписались на канал!", show_alert=True)


