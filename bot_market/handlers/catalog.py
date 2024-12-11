import logging

import dotenv
from aiogram import F
from aiogram import Router, types
from aiogram.types import CallbackQuery, FSInputFile

import loader
from keyboards.inline_kb import generate_category_keyboard
from callbacks.callbacks import CategoryCbData, CategoryPageCbData, SubCategoryPageCbData
from utils.db_utils import Database

from loader import ITEM_PER_PAGE_CATEGORY, ITEM_PER_PAGE_SUBCATEGORY

dotenv.load_dotenv()
catalog = Router()
db = Database(loader.dsn)
photo_path = loader.photo_path_menu


@catalog.message(F.text == 'Каталог')
async def show_categories(message: types.Message):
    try:
        await db.create_pool()
        page = 0
        buttons_text, id = await db.get_categories()
        dict_id = dict(zip(buttons_text, id))
        keyboard = await generate_category_keyboard(page=page,
                                                    dict_id=dict_id,
                                                    buttons_text=buttons_text,
                                                    ITEMS_PER_PAGE=ITEM_PER_PAGE_CATEGORY)

        photo_file = FSInputFile(photo_path)

        await message.answer_photo(
            photo=photo_file,
            caption="Выберите Категорию:",
            reply_markup=keyboard
        )
    except Exception as _ex:
        logging.debug(_ex)
    finally:
        await db.close_pool()


@catalog.callback_query(CategoryCbData.filter())
async def handle_category(callback: CallbackQuery, callback_data: CategoryCbData):
    try:
        await db.create_pool()
        data = callback_data
        logging.debug('Сработал Обработчик Подкатегории')
        logging.debug(data)
        buttons_text, id = await db.get_categories()
        dict_id = dict(zip(buttons_text, id))
        category_name = data.name
        subcategories, sub_id = await db.get_subcategories((dict_id[f'{category_name}']))
        dict_id_cub = dict(zip(subcategories, sub_id))

        if subcategories:
            page = 0
            page_data = CategoryPageCbData(number=0)
            keyboard = await generate_category_keyboard(page=page,
                                                        buttons_text=subcategories,
                                                        dict_id=dict_id_cub,
                                                        subcategory=True,
                                                        ITEMS_PER_PAGE=ITEM_PER_PAGE_SUBCATEGORY,
                                                        category_name=data.name,
                                                        previous_menu_callback=True,
                                                        previous_menu_callback_name=page_data.pack())

            photo_file = FSInputFile(photo_path)

            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo_file,
                    caption="Выберите Подкатегорию:"
                ),
                reply_markup=keyboard
            )

            await callback.answer()
        else:
            await callback.answer("Подкатегории не найдены.", show_alert=True)
    except Exception as _ex:
        logging.debug(_ex)
    finally:
        await db.close_pool()


@catalog.callback_query(CategoryPageCbData.filter())
async def handle_page(callback: CallbackQuery, callback_data: CategoryPageCbData):
    try:
        await db.create_pool()
        data = callback_data.number
        buttons_text, id = await db.get_categories()
        dict_id = dict(zip(buttons_text, id))
        logging.debug('Сработал Обработчик пагинации')
        page = data
        keyboard = await generate_category_keyboard(page=page,
                                                    dict_id=dict_id,
                                                    buttons_text=buttons_text,
                                                    ITEMS_PER_PAGE=ITEM_PER_PAGE_CATEGORY)

        photo_file = FSInputFile(photo_path)

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo_file,
                caption="Выберите категорию:"
            ),
            reply_markup=keyboard
        )
    finally:
        await db.close_pool()


@catalog.callback_query(SubCategoryPageCbData.filter())
async def handle_subcategory_page(callback: CallbackQuery, callback_data: SubCategoryPageCbData):

    try:
        await db.create_pool()
        data = callback_data.number
        buttons_text, id = await db.get_categories()
        dict_id = dict(zip(buttons_text, id))
        logging.debug('Сработал Обработчик пагинации Подкатегории')
        category_name = callback_data.name
        # logging.debug((dict_id[f'{category_name}']))
        subcategories, sub_id = await db.get_subcategories((dict_id[f'{category_name}']))
        dict_id_cub = dict(zip(subcategories, sub_id))

        if subcategories:
            page = data
            page_data = CategoryPageCbData(number=0)
            keyboard = await generate_category_keyboard(page=page,
                                                        buttons_text=subcategories,
                                                        dict_id=dict_id_cub,
                                                        subcategory=True,
                                                        category_name=callback_data.name,
                                                        ITEMS_PER_PAGE=ITEM_PER_PAGE_SUBCATEGORY,
                                                        previous_menu_callback=True,
                                                        previous_menu_callback_name=page_data.pack())

            photo_file = FSInputFile(photo_path)

            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo_file,
                    caption="Выберите Подкатегорию:"
                ),
                reply_markup=keyboard
            )

            await callback.answer()
    except ValueError:
        await callback.answer("Ошибка! Неверный номер страницы.", show_alert=True)
    finally:
        await db.close_pool()
