import asyncio
import logging
import sys

from handlers.faq import faq
from handlers.cart import cart
from handlers.confirm_order import confirm_order
from handlers.payments import payments
from handlers.product_to_cart import product_to_cart
from handlers.catalog import catalog
from handlers.products import products
from handlers.registration import register
from handlers.start import start_router
from loader import dp, bot
from middleware.check_registration import CheckRegistrationMiddleware
from middleware.check_subscription import CheckSubscriptionMiddleware


async def main() -> None:
    dp.include_router(start_router)
    dp.include_router(catalog)
    dp.include_router(register)
    dp.include_router(products)
    dp.include_router(product_to_cart)
    dp.include_router(confirm_order)
    dp.include_router(cart)
    dp.include_router(payments)
    dp.include_router(faq)

    catalog.message.middleware(CheckSubscriptionMiddleware(bot))
    catalog.message.middleware(CheckRegistrationMiddleware(bot))

    products.message.middleware(CheckSubscriptionMiddleware(bot))
    products.message.middleware(CheckRegistrationMiddleware(bot))

    cart.message.middleware(CheckSubscriptionMiddleware(bot))
    cart.message.middleware(CheckRegistrationMiddleware(bot))

    product_to_cart.message.middleware(CheckSubscriptionMiddleware(bot))
    product_to_cart.message.middleware(CheckRegistrationMiddleware(bot))

    confirm_order.message.middleware(CheckSubscriptionMiddleware(bot))
    confirm_order.message.middleware(CheckRegistrationMiddleware(bot))

    payments.message.middleware(CheckSubscriptionMiddleware(bot))
    payments.message.middleware(CheckRegistrationMiddleware(bot))

    faq.message.middleware(CheckSubscriptionMiddleware(bot))
    faq.message.middleware(CheckRegistrationMiddleware(bot))


    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())

