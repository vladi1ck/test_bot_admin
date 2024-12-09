from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def main_kb():
    kb_list = []
    main_menu_buttons_text = ['Каталог', 'Корзина', 'FAQ']

    kb_list.append([KeyboardButton(text=main_menu_buttons_text[0]),
                    KeyboardButton(text=main_menu_buttons_text[1])])

    kb_list.append([KeyboardButton(text=main_menu_buttons_text[2],
                                   colspan=2)])

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=False)
    return keyboard

