import logging

from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

import loader
from callbacks.callbacks import ProductToCartQuantityConfirmation, ProductToCart, CategoryPageCbData, \
    ProductToCartQuantity
from keyboards.inline_kb import generate_product_with_quantity_keyboard
from utils.db_utils import Database

db = Database(loader.dsn)
product_to_cart = Router()

@product_to_cart.callback_query(ProductToCart.filter())
async def handle_product(callback: CallbackQuery, callback_data: ProductToCart):
    try:
        await db.create_pool()
        logging.debug('Сработал Обработчик Продукта в корзину')
        buttons_text, product_id, description_text, photo_url, price = await db.get_product_by_id(callback_data.id)
        if callback_data.name:

            try:
                page = 0
                page_data = CategoryPageCbData(number=0)
                messages = await generate_product_with_quantity_keyboard(page=page,
                                                           buttons_text=[callback_data.name],
                                                           photo_url=[photo_url],
                                                           price=[callback_data.price],
                                                           product_id=[callback_data.id],
                                                           description_text=[callback_data.description],
                                                           subcategory=callback_data.id,
                                                           ITEMS_PER_PAGE=1,
                                                           previous_menu_callback=True,
                                                           previous_menu_callback_name=page_data.pack()
                                                           )
                msg = messages[0]
                photo_path = msg["photo"]
                photo_file = FSInputFile(photo_path[0])
                await callback.message.edit_media(
                    media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
                    reply_markup=msg["reply_markup"]
                )

            except Exception as _ex:
                logging.exception("Ошибка при обработке продукта")
                await callback.answer("Ошибка! Попробуйте снова.", show_alert=True)
        else:
            await callback.answer("Ошибка при получении данных", show_alert=True)
    except:
        logging.exception("Ошибка")
        await callback.answer("Ошибка", show_alert=True)
    finally:
        await db.close_pool()



@product_to_cart.callback_query(ProductToCartQuantity.filter())
async def handle_products_quantity(callback: CallbackQuery, callback_data: ProductToCartQuantity):
    try:
        await db.create_pool()

        logging.debug('Сработал Обработчик количества Продуктов в корзину')
        buttons_text, product_id, description_text, photo_url, price = await db.get_product_by_id(callback_data.id)
        quantity =  callback_data.quantity
        if callback_data.command == -1:
            quantity-=1
            if quantity<0:
                return await callback.answer()
        elif callback_data.command == 1:
            quantity+=1

        if callback_data.name:
            try:
                page = 0
                page_data = CategoryPageCbData(number=0)
                messages = await generate_product_with_quantity_keyboard(page=page,
                                                           buttons_text=[callback_data.name],
                                                           photo_url=[photo_url],
                                                           price=[callback_data.price],
                                                           product_id=[callback_data.id],
                                                           description_text=description_text,
                                                           subcategory=callback_data.id,
                                                           quantity=quantity,
                                                           ITEMS_PER_PAGE=1,
                                                           previous_menu_callback=True,
                                                           previous_menu_callback_name=page_data.pack()
                )
                msg = messages[0]
                photo_path = msg["photo"]
                photo_file = FSInputFile(photo_path[0])
                await callback.message.edit_media(
                    media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
                    reply_markup=msg["reply_markup"]
                )

            except Exception as _ex:
                logging.exception("Ошибка при обработке продукта")
                await callback.answer("Ошибка! Попробуйте снова.", show_alert=True)
        else:
            logging.exception("Ошибка при получении данных'")
            await callback.answer("Ошибка при получении данных", show_alert=True)
    except:
        logging.exception("Ошибка!")
        await callback.answer("Ошибка!", show_alert=True)
    finally:
        await db.close_pool()


@product_to_cart.callback_query(ProductToCartQuantityConfirmation.filter())
async def handle_products_quantity(callback: CallbackQuery, callback_data: ProductToCartQuantityConfirmation):
    try:
        await db.create_pool()

        logging.debug('Сработал Обработчик подтверждения количества Продуктов в корзину')
        buttons_text, product_id, description_text, photo_url, price = await db.get_product_by_id(callback_data.id)
        quantity =  callback_data.quantity
        if product_id and quantity != 0:
            try:
                await db.add_product_to_cart(callback.from_user.id, quantity, product_id[0])
                page = 0
                page_data = CategoryPageCbData(number=0)
                messages = await generate_product_with_quantity_keyboard(page=page,
                                                           buttons_text=buttons_text,
                                                           photo_url=[photo_url],
                                                           price=price,
                                                           product_id=[callback_data.id],
                                                           description_text=description_text,
                                                           subcategory=callback_data.id,
                                                           quantity=quantity,
                                                           confirmation_done=True,
                                                           ITEMS_PER_PAGE=1,
                                                           previous_menu_callback=True,
                                                           previous_menu_callback_name=page_data.pack()
                )
                msg = messages[0]
                photo_path = msg["photo"]
                photo_file = FSInputFile(photo_path[0])
                await callback.message.edit_media(
                    media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
                    reply_markup=msg["reply_markup"]
                )

            except Exception as _ex:
                logging.exception("Ошибка при обработке продукта")
                await callback.answer("Ошибка! Попробуйте снова.", show_alert=True)
        elif quantity == 0:
            await callback.answer("Количество должно быть отлично от 0", show_alert=True)
        else:
            logging.exception("Ошибка при получении данных")
            await callback.answer("Ошибка при получении данных", show_alert=True)
    except:
        logging.exception("Ошибка!")
        await callback.answer("Ошибка!", show_alert=True)
    finally:
        await db.close_pool()