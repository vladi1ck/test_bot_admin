import logging

from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, \
    InputMediaPhoto

import loader
from callbacks.callbacks import SubCategoryCbData, \
    CategoryPageCbData, ProductPageCbData, BackToMenu
from keyboards.inline_kb import generate_product_keyboard
from utils.db_utils import Database

db = Database(loader.dsn)
products = Router()

@products.callback_query(SubCategoryCbData.filter())
async def handle_product(callback: CallbackQuery, callback_data: SubCategoryCbData):
    await db.create_pool()

    buttons_text, product_id, description_text,photo_url, price  = await db.get_products(callback_data.id)
    logging.debug('Сработал Обработчик Продукта')
    try:
        if buttons_text:
            try:
                page = 0
                page_data = CategoryPageCbData(number=0)
                messages = await generate_product_keyboard(page=page,
                                                            buttons_text=buttons_text,
                                                            description_text=description_text,
                                                            photo_url=photo_url,
                                                            price=price,
                                                            product_id=product_id,
                                                            subcategory=callback_data.id,
                                                            ITEMS_PER_PAGE=1,
                                                            previous_menu_callback = True,
                                                            previous_menu_callback_name = page_data.pack()
                )
                msg = messages[0]
                photo_path = msg["photo"]
                photo_file = FSInputFile(photo_path)

                await callback.message.edit_media(
                    media=InputMediaPhoto(media=photo_file, caption=msg["caption"]),
                    reply_markup=msg["reply_markup"]
                )

            except Exception as _ex:
                logging.debug(_ex)
        else:
            try:
                await callback.answer("Товары не найдены.", show_alert=True)
            except Exception as e:
                logging.error(f"Ошибка при отправке alert: {e}")
    finally:
        await db.close_pool()


@products.callback_query(ProductPageCbData.filter())
async def handle_product(callback: CallbackQuery, callback_data: ProductPageCbData):
    await callback.answer()
    await db.create_pool()

    buttons_text, product_id, description_text,photo_url, price  = await db.get_products(callback_data.id)
    logging.debug('Сработал Обработчик Продукта пагинации')

    try:
        page = callback_data.number
        page_data = CategoryPageCbData(number=0)
        messages = await generate_product_keyboard(page=page,
                                                    buttons_text=buttons_text,
                                                    description_text=description_text,
                                                    photo_url=photo_url,
                                                    price=price,
                                                    product_id=product_id,
                                                    subcategory=callback_data.id,
                                                    ITEMS_PER_PAGE=1,
                                                    previous_menu_callback = True,
                                                    previous_menu_callback_name = page_data.pack()
        )
        logging.debug(len(messages))
        msg = messages[0]
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


@products.callback_query(BackToMenu.filter())
async def handle_back_to_menu(callback: CallbackQuery, callback_data: BackToMenu):
    data = callback_data.name
    try:
        await callback.answer()

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться", callback_data="return_to_main_menu")]
        ])

        if callback.message.photo:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=FSInputFile("C:/Users/user/PycharmProjects/bot_admin/admin_panel/media/menu.jpg"),
                    caption="Выберите категорию:"  # Текст главного меню
                ),
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(
                text="Выберите категорию:",
                reply_markup=keyboard
            )
    except Exception as e:
        logging.exception("Ошибка при обработке кнопки 'Назад к меню'")
        await callback.answer("Ошибка при возвращении в меню", show_alert=True)
