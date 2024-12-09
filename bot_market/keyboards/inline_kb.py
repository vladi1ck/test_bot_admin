import logging
import math
from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.callbacks import CategoryCbData, SubCategoryPageCbData, CategoryPageCbData, SubCategoryCbData, \
    ProductToCart, ProductPageCbData, ProductToCartQuantityConfirmationDone, ProductToCartQuantity, \
    ProductToCartQuantityConfirmation, CartDeleteItem, CartChangeItem, CartChangeItemConfirm, \
    ChangeProductToCartQuantity, CartPageCbData, DeleteAllItemsFromCart, CartConfirmOrder


async def generate_category_keyboard(page: int,
                                     buttons_text: [],
                                     dict_id: {}=None,
                                     subcategory: bool=False,
                                     category_name:str='',
                                     ITEMS_PER_PAGE: int = 2,
                                     previous_menu_callback: bool = False,
                                     previous_menu_callback_name: str=None) -> InlineKeyboardMarkup:
    total_pages = math.ceil(len(buttons_text) / ITEMS_PER_PAGE)
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    items_on_page = buttons_text[start_index:end_index]
    builder = InlineKeyboardBuilder()

    for item in items_on_page:
        logging.debug(item)
        if subcategory:
            data_name = SubCategoryCbData(name=item, id=dict_id[f'{item}'])
            builder.button(
                text=item,
                callback_data=data_name.pack()
            )
        else:
            data_name = CategoryCbData(name=item, id=dict_id[f'{item}'])
            builder.button(
                text=item,
                callback_data=data_name.pack()
            )


    if page > 0:
        if subcategory:
            page_data = SubCategoryPageCbData(number=page - 1, name=category_name)
            builder.button(text="⬅ Назад", callback_data=page_data.pack())
        else:
            page_data = CategoryPageCbData(number=page - 1)
            builder.button(text="⬅ Назад", callback_data=page_data.pack())
    if page < total_pages - 1:
        if subcategory:
            page_data = SubCategoryPageCbData(number=page + 1, name=category_name)
            builder.button(text="Вперёд ➡", callback_data=page_data.pack())
        else:
            page_data = CategoryPageCbData(number=page + 1)
            builder.button(text="Вперёд ➡", callback_data=page_data.pack())


    if previous_menu_callback:
        builder.button(
            text="🔙 Назад к меню",
            callback_data=previous_menu_callback_name
        )

    builder.adjust(1)
    return builder.as_markup()



async def generate_product_keyboard(page: int,
                                     buttons_text: [],
                                     ITEMS_PER_PAGE: int = 2,
                                     description_text: []=None,
                                     photo_url: []=None,
                                     price: []=None,
                                     product_id: []=None,
                                     subcategory: int=0,
                                     dict_id: {}=None,
                                     previous_menu_callback: bool = True,
                                     previous_menu_callback_name: str='') -> list[
    dict[str, InlineKeyboardMarkup | str | Any]]:

    total_pages = math.ceil(len(buttons_text) / ITEMS_PER_PAGE)
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE


    items_on_page = buttons_text[start_index:end_index]
    photos_on_page = photo_url[start_index:end_index]
    prices_on_page = price[start_index:end_index]
    desc_on_page = description_text[start_index:end_index]
    id_on_page = product_id[start_index:end_index]

    messages = []

    for item, photo, price, description, id in zip(items_on_page, photos_on_page, prices_on_page, desc_on_page, id_on_page):
        builder = InlineKeyboardBuilder()

        data_name = ProductToCart(name=item,
                                  id=id,
                                  price=price,
                                  description=description,
        )
        builder.button(
            text=f"Купить {item}",
            callback_data=data_name.pack()
        )

        if page > 0:
            page_data = ProductPageCbData(number=page - 1, id=subcategory)
            builder.button(text="⬅ Назад", callback_data=page_data.pack())
        if page < total_pages - 1:
            page_data = ProductPageCbData(number=page + 1, id=subcategory)
            builder.button(text="Вперёд ➡", callback_data=page_data.pack())

        if previous_menu_callback:
            builder.button(
                text="🔙 Назад к меню",
                callback_data=previous_menu_callback_name
            )

        builder.adjust(1)

        messages.append({
            "photo": photo,
            "caption": f"**{item}**\nОписание: {description}\nЦена: {price}",
            "reply_markup": builder.as_markup()
        })

    return messages


async def generate_product_with_quantity_keyboard(page: int,
                                     buttons_text: [],
                                     ITEMS_PER_PAGE: int = 2,
                                     description_text: []=None,
                                     photo_url: []=None,
                                     price: []=None,
                                     product_id: []=None,
                                     quantity:int=0,
                                     subcategory: int=0,
                                     dict_id: {}=None,
                                     previous_menu_callback: bool = True,
                                     confirmation_done: bool=False,
                                     previous_menu_callback_name: str='') -> list[
    dict[str, InlineKeyboardMarkup | str | Any]]:

    total_pages = math.ceil(len(buttons_text) / ITEMS_PER_PAGE)
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE


    items_on_page = buttons_text[start_index:end_index]
    photos_on_page = photo_url[start_index:end_index]
    prices_on_page = price[start_index:end_index]
    desc_on_page = description_text[start_index:end_index]
    id_on_page = product_id[start_index:end_index]

    messages = []

    for item, photo, price, description, id in zip(items_on_page, photos_on_page, prices_on_page, desc_on_page, id_on_page):
        builder = InlineKeyboardBuilder()
        if confirmation_done:
            builder.button(text=f'Товар успешно добавлен в корзину!', callback_data='fdf')
            builder.button(text=f' ', callback_data='fdf')
            go_to_cart = ProductToCartQuantityConfirmationDone(id=1)
            builder.button(text=f'Перейти в корзину', callback_data=go_to_cart.pack())
        else:
            data_name_inc = ProductToCartQuantity(name=item, id=id, price=price, command=1, quantity=quantity)
            data_name_dec = ProductToCartQuantity(name=item, id=id, price=price, command=-1, quantity=quantity)
            builder.button(text=f'Количество:{quantity}', callback_data='cscac')
            builder.button(text='+1 Товар', callback_data=data_name_inc.pack())
            builder.button(text='-1 Товар', callback_data=data_name_dec.pack())

            data_confirm = ProductToCartQuantityConfirmation(id=id, quantity=quantity)
            builder.button(text='Подтвердить количество', callback_data=data_confirm.pack())

        if previous_menu_callback:
            builder.button(
                text="🔙 Назад к меню",
                callback_data=previous_menu_callback_name
            )

        builder.adjust(1)
        messages.append({
            "photo": photo,
            "caption": f"**{item}**\nОписание: {description}\nЦена: {price}\nСумма: {quantity*price}",
            "reply_markup": builder.as_markup()
        })

    return messages

async def generate_cart_keyboard(page:int=0,
                                 data:[]=None,
                                 ITEMS_PER_PAGE:int=4,
                                 quantity:int=0,
                                 previous_menu_callback: bool = True,
                                 previous_menu_callback_name: str = ''
    ):
    total_pages = math.ceil(len(data) / ITEMS_PER_PAGE)
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    builder = InlineKeyboardBuilder()
    sum_data=[]
    if len(data) != 0:
        buttons_text = data[start_index:end_index]
        for item in buttons_text:
            product = item['product_name']
            quantity = item['quantity']
            builder.row(InlineKeyboardButton(text=f'{product}: кол-во: {quantity}', callback_data='dasdasda'))
            delete_item = CartDeleteItem(cart_item_id=item['cart_item_id'])
            change_item = CartChangeItem(cart_item_id=item['cart_item_id'])
            builder.row(
                InlineKeyboardButton(text='Изменить', callback_data=change_item.pack()),
                InlineKeyboardButton(text='Удалить', callback_data=delete_item.pack()),
            )
            sum_data.append(item['product_price']*quantity)
    else:
        builder.row(InlineKeyboardButton(text='Корзина пуста', callback_data='dasdasda'))
    builder.row(InlineKeyboardButton(text=' ', callback_data='fdf'))
    builder.row(InlineKeyboardButton(text=f'Сумма: {sum(sum_data)}', callback_data='fdf'))

    if page > 0:
        page_data = CartPageCbData(number=page - 1)
        builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data=page_data.pack()))
    if page < total_pages - 1:
        page_data = CartPageCbData(number=page + 1)
        builder.row(InlineKeyboardButton(text="Вперёд ➡", callback_data=page_data.pack()))


    delete_all_items = DeleteAllItemsFromCart(cart_item_id=0)
    if previous_menu_callback:
        builder.row(
            InlineKeyboardButton(
                text="Очистить корзину",
                callback_data=delete_all_items.pack()
            ),
            InlineKeyboardButton(
                text="Вернуться назад",
                callback_data=previous_menu_callback_name
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="Очистить корзину",
                callback_data=delete_all_items.pack()
            )
        )
    if len(data) != 0:
        confirm_order = CartConfirmOrder(sum=sum(sum_data))
        builder.row(
            InlineKeyboardButton(
                text="Перейти к оформлению",
                callback_data=confirm_order.pack()
            )
        )

    return builder.as_markup()

async def generate_cart_change_quantity_keyboard(page: int,
                                     buttons_text: [],
                                     ITEMS_PER_PAGE: int = 2,
                                     description_text: []=None,
                                     photo_url: []=None,
                                     price: []=None,
                                     product_id: []=None,
                                     quantity:int=0,
                                     new_quantity:int=0,
                                     cart_item_id:int=0,
                                     subcategory: int=0,
                                     dict_id: {}=None,
                                     previous_menu_callback: bool = True,
                                     confirmation_done: bool=False,
                                     previous_menu_callback_name: str='') -> list[
    dict[str, InlineKeyboardMarkup | str | Any]]:

    total_pages = math.ceil(len(buttons_text) / ITEMS_PER_PAGE)
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE


    items_on_page = buttons_text[start_index:end_index]
    photos_on_page = photo_url[start_index:end_index]
    prices_on_page = price[start_index:end_index]
    desc_on_page = description_text[start_index:end_index]
    id_on_page = product_id[start_index:end_index]

    messages = []

    for item, photo, price, description, id in zip(items_on_page, photos_on_page, prices_on_page, desc_on_page, id_on_page):
        builder = InlineKeyboardBuilder()
        if confirmation_done:
            builder.button(text=f'Товар успешно изменен в корзине!', callback_data='fdf')
            builder.button(text=f' ', callback_data='fdf')
            go_to_cart = ProductToCartQuantityConfirmationDone(id=1)
            builder.button(text=f'Перейти в корзину', callback_data=go_to_cart.pack())
        else:
            data_name_inc = ChangeProductToCartQuantity(cart_item_id=cart_item_id, command=1, quantity=quantity)
            data_name_dec = ChangeProductToCartQuantity(cart_item_id=cart_item_id, command=-1, quantity=quantity)
            builder.button(text=f'Количество:{quantity}', callback_data='cscac')
            builder.button(text='+1 Товар', callback_data=data_name_inc.pack())
            builder.button(text='-1 Товар', callback_data=data_name_dec.pack())

            data_confirm = CartChangeItemConfirm(cart_item_id=cart_item_id, quantity=quantity)
            builder.button(text='Подтвердить количество', callback_data=data_confirm.pack())

        if previous_menu_callback:
            builder.button(
                text="🔙 Назад к меню",
                callback_data=previous_menu_callback_name
            )

        builder.adjust(1)
        messages.append({
            "photo": photo,
            "caption": f"**{item}**\nОписание: {description}\nЦена: {price}\nСумма: {quantity*price}",
            "reply_markup": builder.as_markup()
        })

    return messages

