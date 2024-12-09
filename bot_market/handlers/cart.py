import logging

from aiogram import Router, F, types
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

import loader
from callbacks.callbacks import CartDeleteItem, CartChangeItem, CategoryPageCbData, CartChangeItemConfirm, \
    ChangeProductToCartQuantity, CartPageCbData, DeleteAllItemsFromCart
from keyboards.inline_kb import ProductToCartQuantityConfirmationDone, generate_cart_keyboard, \
    generate_cart_change_quantity_keyboard
from utils.db_utils import Database

db = Database(loader.dsn)
cart = Router()
photo_path = loader.photo_path_cart

@cart.message(F.text == 'Корзина')
async def show_categories(message: types.Message):
    try:
        await db.create_pool()
        data = await db.get_cart_items(message.from_user.id)
        logging.debug(f'data - {data}')
        page_data = CategoryPageCbData(number=0)
        keyboard = await generate_cart_keyboard(data=data,
                                                previous_menu_callback=True,
                                                previous_menu_callback_name=page_data.pack()
        )
        photo_file = FSInputFile(photo_path)

        await message.answer_photo(
            photo=photo_file,
            caption="Корзина",
            reply_markup=keyboard
        )
    except Exception as _ex:
        logging.debug(_ex)
    finally:
        await db.close_pool()

@cart.callback_query(CartPageCbData.filter())
async def show_cart(callback: CallbackQuery, callback_data: CartPageCbData):
    try:
        await db.create_pool()
        data = await db.get_cart_items(callback.from_user.id)
        logging.debug(f'data - {data}')

        keyboard = await generate_cart_keyboard(page=callback_data.number, data=data)
        photo_file = FSInputFile(photo_path)

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo_file,
                caption="Корзина:"
            ),
            reply_markup=keyboard
        )

    except Exception as _ex:
        logging.debug(_ex)
    finally:
        await db.close_pool()

@cart.callback_query(ProductToCartQuantityConfirmationDone.filter())
async def handle_back_to_menu_cart(callback: CallbackQuery, callback_data: ProductToCartQuantityConfirmationDone):
    try:
        await db.create_pool()
        data = await db.get_cart_items(callback.from_user.id)
        logging.debug(f'data - {data}')
        page_data = CategoryPageCbData(number=0)
        keyboard = await generate_cart_keyboard(data=data,
                                                previous_menu_callback=True,
                                                previous_menu_callback_name=page_data.pack()
        )
        photo_file = FSInputFile(photo_path)

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo_file,
                caption="Корзина:"
            ),
            reply_markup=keyboard
        )
    except Exception as e:
        logging.exception("Ошибка при обработке кнопки 'Назад к меню'")
        await callback.answer("Ошибка при возвращении в меню", show_alert=True)
        await db.close_pool()

@cart.callback_query(CartDeleteItem.filter())
async def handle_delete_item_from_cart(callback: CallbackQuery, callback_data: CartDeleteItem):
    try:
        await db.create_pool()
        cart_item_id = callback_data.cart_item_id
        await db.delete_item_from_cart(cart_item_id)
        data = await db.get_cart_items(callback.from_user.id)
        logging.debug(f'data - {data}')
        page_data = CategoryPageCbData(number=0)
        keyboard = await generate_cart_keyboard(data=data,
                                                previous_menu_callback=True,
                                                previous_menu_callback_name=page_data.pack()
                                                )
        photo_file = FSInputFile(photo_path)

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo_file,
                caption="Корзина:"
            ),
            reply_markup=keyboard
        )
    except Exception as e:
        logging.exception("Ошибка при обработке кнопки 'Назад к меню'")
        await callback.answer("Ошибка при возвращении в меню", show_alert=True)
        await db.close_pool()

@cart.callback_query(CartChangeItem.filter())
async def handle_change_item_from_cart(callback: CallbackQuery, callback_data: CartChangeItem):
    try:
        await db.create_pool()
        cart_item_id = callback_data.cart_item_id
        data_row = await db.get_cart_item(cart_item_id)
        if data_row is not None:
            data = data_row[0]
        logging.debug(f'data - {data}')

        page = 0
        page_data = CategoryPageCbData(number=0)
        messages = await generate_cart_change_quantity_keyboard(page=page,
                                                                 buttons_text=[data['product_name']],
                                                                 photo_url=[data['product_image_absolute_path']],
                                                                 price=[data['product_price']],
                                                                 product_id=[data['product_id']],
                                                                 description_text=[data['product_description']],
                                                                 cart_item_id=data['cart_item_id'],
                                                                 quantity=data['quantity'],
                                                                 ITEMS_PER_PAGE=1,
                                                                 previous_menu_callback=True,
                                                                 previous_menu_callback_name=page_data.pack()
                                                                 )
        logging.debug(len(messages))
        msg = messages[0]
        logging.debug(msg)
        photo_path = msg["photo"]
        photo_file = FSInputFile(photo_path)
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
            reply_markup=msg["reply_markup"]
        )

    except Exception as e:
        logging.exception("Ошибка при обработке кнопки 'Назад к меню'")
        await callback.answer("Ошибка при возвращении в меню", show_alert=True)
        await db.close_pool()



@cart.callback_query(ChangeProductToCartQuantity.filter())
async def handle_products_change_quantity(callback: CallbackQuery, callback_data: ChangeProductToCartQuantity):
    try:
        await db.create_pool()
        cart_item_id = callback_data.cart_item_id
        data_row = await db.get_cart_item(cart_item_id)
        logging.debug(data_row)
        logging.debug(callback_data)
        if data_row is not None:
            data = data_row[0]
        logging.debug(f'data - {data}')
        logging.debug('Сработал Обработчик')

        quantity =  callback_data.quantity
        if callback_data.command == -1:
            quantity-=1
            if quantity<0:
                return await callback.answer()
        elif callback_data.command == 1:
            quantity+=1

        if callback_data.quantity:
            try:
                page = 0
                page_data = CategoryPageCbData(number=0)
                messages = await generate_cart_change_quantity_keyboard(page=page,
                                                                        buttons_text=[data['product_name']],
                                                                        photo_url=[data['product_image_absolute_path']],
                                                                        price=[data['product_price']],
                                                                        product_id=[data['product_id']],
                                                                        description_text=[data['product_description']],
                                                                        cart_item_id=data['cart_item_id'],
                                                                        quantity=quantity,
                                                                        new_quantity=quantity,
                                                                        ITEMS_PER_PAGE=1,
                                                                        previous_menu_callback=True,
                                                                        previous_menu_callback_name=page_data.pack()
                                                                        )
                logging.debug(len(messages))
                msg = messages[0]
                logging.debug(msg)
                photo_path = msg["photo"]
                photo_file = FSInputFile(photo_path)
                await callback.message.edit_media(
                    media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
                    reply_markup=msg["reply_markup"]
                )

            except Exception as _ex:
                logging.exception("Ошибка при обработке продукта")
                await callback.answer("Ошибка! Попробуйте снова.", show_alert=True)
            finally:
                await db.close_pool()
        else:
            logging.exception("Ошибка при обработке кнопки 'Назад к меню'")
            await callback.answer("Ошибка при возвращении в меню", show_alert=True)
    except:
        logging.exception("Ошибка!")
        await callback.answer("Ошибка!", show_alert=True)



@cart.callback_query(CartChangeItemConfirm.filter())
async def handle_confirm_change_item_from_cart(callback: CallbackQuery, callback_data: CartChangeItemConfirm):
    try:
        await db.create_pool()
        cart_item_id = callback_data.cart_item_id
        await db.change_item_from_cart(callback_data.quantity, cart_item_id)
        data_row = await db.get_cart_item(cart_item_id)
        if data_row is not None:
            data = data_row[0]
        logging.debug(f'data - {data}')

        page = 0
        page_data = CategoryPageCbData(number=0)
        messages = await generate_cart_change_quantity_keyboard(page=page,
                                                                 buttons_text=[data['product_name']],
                                                                 photo_url=[data['product_image_absolute_path']],
                                                                 price=[data['product_price']],
                                                                 product_id=[data['product_id']],
                                                                 description_text=[data['product_description']],
                                                                 quantity=callback_data.quantity,
                                                                 confirmation_done=True,
                                                                 ITEMS_PER_PAGE=1,
                                                                 previous_menu_callback=True,
                                                                 previous_menu_callback_name=page_data.pack()
                                                                 )
        logging.debug(len(messages))
        msg = messages[0]
        logging.debug(msg)
        photo_path = msg["photo"]
        photo_file = FSInputFile(photo_path)
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
            reply_markup=msg["reply_markup"]
        )

    except Exception as e:
        logging.exception("Ошибка при обработке кнопки 'Назад к меню'")
        await callback.answer("Ошибка при возвращении в меню", show_alert=True)
        await db.close_pool()


@cart.callback_query(DeleteAllItemsFromCart.filter())
async def delete_items_and_show_cart(callback: CallbackQuery, callback_data: DeleteAllItemsFromCart):
    try:
        await db.create_pool()
        await db.delete_all_items_from_cart(callback.from_user.id)
        data = await db.get_cart_items(callback.from_user.id)
        logging.debug(f'data - {data}')

        page_data = CategoryPageCbData(number=0)
        keyboard = await generate_cart_keyboard(page=0,
                                                data=data,
                                                previous_menu_callback=True,
                                                previous_menu_callback_name=page_data.pack()
        )
        photo_file = FSInputFile(photo_path)

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo_file,
                caption="Корзина:"
            ),
            reply_markup=keyboard
        )

    except Exception as _ex:
        logging.debug(_ex)
    finally:
        await db.close_pool()


