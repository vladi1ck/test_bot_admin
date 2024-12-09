import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

import loader
from callbacks.callbacks import CartConfirmOrder, Payments
from states.cart_address_state import AddressState
from utils.db_utils import Database

confirm_order = Router()
db = Database(loader.dsn)


@confirm_order.callback_query(CartConfirmOrder.filter())
async def enter_address(callback: types.CallbackQuery, callback_data: CartConfirmOrder, state: FSMContext):
    await db.create_pool()
    try:
        address = await db.get_users_address(callback.from_user.id)
    except Exception as ex:
        logging.error(f"Ошибка получения адреса пользователя: {ex}")
        await callback.message.answer("Произошла ошибка при получении вашего адреса. Попробуйте снова позже.")
        return
    finally:
        await db.close_pool()

    if address:
        # Адрес уже есть, предлагаем подтвердить или изменить
        payments_data = Payments(sum=callback_data.sum)
        await state.update_data(sum=callback_data.sum)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Подтвердить", callback_data=payments_data.pack())],
                [InlineKeyboardButton(text="Изменить", callback_data="edit_address")],
            ]
        )
        await callback.message.answer(
            f"Вы указали адрес:\n\n"
            f"Город - {address['city']}\n"
            f"Улица - {address['street']}\n"
            f"Дом - {address['house']}\n"
            f"Квартира - {address['apartment']}\n\n"
            f"Подтвердите или измените:",
            reply_markup=keyboard
        )
    else:
        # Если адреса нет, начинаем сбор данных
        await callback.message.answer("Введите название вашего города:")
        await state.update_data(sum=callback_data.sum)
        await state.set_state(AddressState.waiting_for_city)
    await callback.answer()


@confirm_order.message(AddressState.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    city = message.text.strip()
    await state.update_data(city=city)

    await message.answer("Введите название улицы:")
    await state.set_state(AddressState.waiting_for_street)


@confirm_order.message(AddressState.waiting_for_street)
async def process_street(message: types.Message, state: FSMContext):
    street = message.text.strip()
    await state.update_data(street=street)

    await message.answer("Введите номер дома:")
    await state.set_state(AddressState.waiting_for_house)


@confirm_order.message(AddressState.waiting_for_house)
async def process_house(message: types.Message, state: FSMContext):
    house = message.text.strip()
    await state.update_data(house=house)

    await message.answer("Введите номер квартиры (или напишите 'нет', если не требуется):")
    await state.set_state(AddressState.waiting_for_apartment)


@confirm_order.message(AddressState.waiting_for_apartment)
async def process_apartment(message: types.Message, state: FSMContext):
    apartment = message.text.strip()
    if apartment.lower() == "нет":
        apartment = None
    await state.update_data(apartment=apartment)

    # Подтверждение адреса
    data = await state.get_data()
    address = f"{data.get('city')}, {data.get('street')}, дом {data.get('house')}"
    if apartment:
        address += f", кв. {apartment}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_address")],
            [InlineKeyboardButton(text="Изменить", callback_data="edit_address")],
        ]
    )
    await message.answer(f"Вы указали адрес:\n\n{address}\n\nПодтвердите или измените:", reply_markup=keyboard)
    await state.set_state(AddressState.waiting_for_confirm)


@confirm_order.callback_query(F.data == "confirm_address")
async def confirm_address(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    try:
        await db.create_pool()
        await db.set_users_address(
            telegram_id=callback.from_user.id,
            city=data['city'],
            street=data['street'],
            house=data['house'],
            apartment=data['apartment']
        )
    except Exception as ex:
        logging.error(f"Ошибка сохранения адреса: {ex}")
        await callback.message.answer("Произошла ошибка при сохранении вашего адреса. Попробуйте снова позже.")
        return
    finally:
        await db.close_pool()

    payments_data = Payments(sum=data.get('sum'))
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти к оплате", callback_data=payments_data.pack())],
        ]
    )

    await callback.message.answer("Адрес успешно сохранен! Переходим к оплате.", reply_markup=keyboard)
    await state.clear()
    await callback.answer()


@confirm_order.callback_query(F.data == "edit_address")
async def edit_address(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название вашего города (начнем заново):")
    await state.set_state(AddressState.waiting_for_city)
    await callback.answer()
