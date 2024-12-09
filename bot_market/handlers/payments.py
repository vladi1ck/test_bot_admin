import logging
from email.headerregistry import ContentTypeHeader
from mailbox import Message

from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, PreCheckoutQuery

import loader
from callbacks.callbacks import Payments
from utils.db_utils import Database

payments = Router()
db = Database(loader.dsn)
photo_path = "C:/Users/user/PycharmProjects/bot_admin/admin_panel/media/cart.png"

@payments.callback_query(Payments.filter())
async def show_cart(callback: CallbackQuery, callback_data: Payments):
    try:
        await loader.bot.send_invoice(chat_id=callback.from_user.id,
                                      title='Оплата',
                                      description='Оплата заказа в Интернет магазине',
                                      payload='payments_order',
                                      provider_token=loader.YOOKASSA_TOKEN,
                                      start_parameter="test",
                                      currency='RUB',
                                      prices=[
                                          {
                                          'label': 'Руб',
                                          'amount': callback_data.sum*100,
                                          }
                                      ]
        )
    except Exception as _ex:
        logging.debug(_ex)
    finally:
        pass

@payments.pre_checkout_query()
async def pre_checkout_order(pre_checkout_query: PreCheckoutQuery):
    await loader.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@payments.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    if message.successful_payment:
        if message.successful_payment.invoice_payload == 'payments_order':

            try:
                await db.create_pool()
                order = await db.create_order(message.from_user.id)
                if order:
                    await db.delete_all_items_from_cart(message.from_user.id)
                    await db.change_order_status(order)
                await message.answer("Платеж успешно завершен! Спасибо за ваш заказ.")
            except Exception as _ex:
                logging.debug(_ex)
            finally:
                await db.close_pool()
    else:
        await message.answer("Произошла ошибка, пожалуйста, повторите попытку.")


