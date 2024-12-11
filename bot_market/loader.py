import os

import dotenv
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


dotenv.load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
POSTGRES_HOST=os.getenv("POSTGRES_HOST", 'docker.internal.host')
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD_LINK=os.getenv("POSTGRES_PASSWORD_LINK")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD_LINK}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
YOOKASSA_TOKEN = os.getenv('YOOKASSA_TOKEN')

ITEM_PER_PAGE_CATEGORY = 3
ITEM_PER_PAGE_SUBCATEGORY = 3

photo_path_menu = "static/menu.jpg"
photo_path_cart = "static/cart.png"
