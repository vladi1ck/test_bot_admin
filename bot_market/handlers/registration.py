from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import loader
from keyboards.main_keyboards import main_kb
from states.register import Registration
from utils.db_utils import Database
from utils.utils import create_phone_button, check_register

register = Router()
db = Database(dsn=loader.dsn)

@register.message(Command('register'))
async def registration(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_register = await check_register(user_id)
    if is_register:
        await message.answer("Вы уже зарегистрированы! \n Выберите действие из меню ", reply_markup=await main_kb())
    else:
        await message.answer('Регистрация:')
        await message.answer("Введите ваше имя:")
        await state.set_state(Registration.first_name)

@register.message(Registration.first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(Registration.last_name)


@register.message(Registration.last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Отлично! Теперь отправьте ваш номер телефона:", reply_markup=await create_phone_button())
    await state.set_state(Registration.phone)


@register.message(Registration.phone)
async def process_phone(message: Message, state: FSMContext):
    await db.create_pool()
    user_data = await state.get_data()
    first_name = user_data.get("first_name")
    last_name = user_data.get('last_name')
    phone = message.contact.phone_number

    await state.clear()
    await db.insert_user_and_create_cart(telegram_id=message.from_user.id,
                      first_name=first_name, last_name=last_name, phone=phone)

    await message.answer('Регистрация завершена успешно!\n '
                         'Выберите действие из меню', reply_markup=await main_kb())
    await db.close_pool()