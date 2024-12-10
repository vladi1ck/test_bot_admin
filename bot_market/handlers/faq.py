import hashlib
import logging

from aiogram import Router, types, F
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.markdown import hbold

from utils.db_utils import Database

import loader


faq = Router()
db = Database(loader.dsn)

@faq.message(F.text == "FAQ")
async def faq_button_handler(message: types.Message):
    await message.answer(
        "Отлично! Введите ваш вопрос в строке инлайн-запроса с именем бота (например, `@botname пароль`).",
    )


@faq.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    results = []
    await db.create_pool()
    faq_items = await db.get_faq()
    await db.close_pool()
    logging.debug(faq_items)

    for question, answer in faq_items.items():
        if query in question.lower():
            result_id = hashlib.md5(question.encode()).hexdigest()
            results.append(
                InlineQueryResultArticle(
                    id=result_id,
                    title=question,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{hbold('Вопрос:')} {question}\n\n{hbold('Ответ:')} {answer}",
                        parse_mode="HTML",
                    ),
                    description=answer[:50],
                )
            )


    await loader.bot.answer_inline_query(inline_query.id, results=results[:10], cache_time=1)
