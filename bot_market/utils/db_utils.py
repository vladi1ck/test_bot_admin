import logging
from datetime import datetime

import asyncpg


class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        logging.info("Pool created")

    async def fetch_data(self, query: str):
        async with self.pool.acquire() as conn:
            result = await conn.fetch(query)
            return result

    async def check_user(self, user_id) -> bool:
        async with self.pool.acquire() as conn:
            try:
                query = f"SELECT * FROM users_telegramuser WHERE telegram_user_id = $1"
                user = await conn.fetchrow(query, user_id)
                logging.debug(user)
                return user is not None
            except Exception as _ex:
                logging.debug(_ex)
                return False

    async def insert_user_and_create_cart(self, telegram_id, first_name, last_name, phone):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    """
                    INSERT INTO users_telegramuser (telegram_user_id, first_name, last_name, phone_number)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (telegram_user_id) DO NOTHING
                    """,
                    telegram_id, first_name, last_name, phone
                )

                user_exists = await connection.fetchval(
                    """
                    SELECT id FROM users_telegramuser WHERE telegram_user_id = $1
                    """,
                    telegram_id
                )
                if not user_exists:
                    raise ValueError(f"User with telegram_user_id {telegram_id} not found.")

                await connection.execute(
                    """
                    INSERT INTO orders_cart (user_id, created_at)
                    VALUES ($1, $2)
                    ON CONFLICT (user_id) DO NOTHING
                    """,
                    user_exists, datetime.now()
                )

    async def set_users_address(self, telegram_id, city, street, house, apartment):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                user_exists = await connection.fetchval(
                    """
                    SELECT id FROM users_telegramuser WHERE telegram_user_id = $1
                    """,
                    telegram_id
                )
                if not user_exists:
                    raise ValueError(f"User with telegram_user_id {telegram_id} not found.")

                await connection.execute(
                    """
                    INSERT INTO users_address (user_id, city, street, house, apartment)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    user_exists, city, street, house, apartment
                )

    async def get_users_address(self, telegram_id):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                user_exists = await connection.fetchval(
                    """
                    SELECT id FROM users_telegramuser WHERE telegram_user_id = $1
                    """,
                    telegram_id
                )
                if not user_exists:
                    raise ValueError(f"User with telegram_user_id {telegram_id} not found.")
                address = await connection.fetch(
                    """
                    SELECT * FROM users_address WHERE user_id = $1
                    """,
                    user_exists,
                )
                address_dict = {}

                for item in address:

                    if item is not None:
                        address_dict['id'] = item[0]
                        address_dict['city'] = item[1]
                        address_dict['street'] = item[2]
                        address_dict['house'] = item[3]
                        address_dict['apartment'] = item[4]

                return address_dict

    async def get_categories(self):
        async with self.pool.acquire() as conn:
            try:
                categories = await conn.fetch("SELECT name, id FROM catalog_category")
                buttons_text = [cat['name'] for cat in categories]
                id = [cat['id'] for cat in categories]
                return buttons_text, id
            except Exception as _ex:
                logging.debug(_ex)

    async def get_subcategories(self, category: int):
        async with self.pool.acquire() as conn:
            try:
                query = f"SELECT * FROM catalog_subcategory WHERE parent_id = $1"
                subcategories = await conn.fetch(query, category)
                logging.debug(subcategories)
                buttons_text = [cat['name'] for cat in subcategories]
                id = [cat['id'] for cat in subcategories]
                return buttons_text, id
            except Exception as _ex:
                logging.debug(_ex)

    async def get_products(self, product: int):
        async with self.pool.acquire() as conn:
            try:
                query = f"SELECT * FROM catalog_product WHERE category_id = $1"
                products = await conn.fetch(query, product)
                logging.debug(products)
                buttons_text = [cat['name'] for cat in products]
                description_text = [cat['description'] for cat in products]
                photo_url = [cat['image_absolute_path'] for cat in products]
                price = [cat['price'] for cat in products]
                id = [cat['id'] for cat in products]
                return buttons_text, id, description_text, photo_url, price
            except Exception as _ex:
                logging.debug(_ex)

    async def get_product_by_id(self, product_id: int):
        async with self.pool.acquire() as conn:
            try:
                query = f"SELECT * FROM catalog_product WHERE id = $1"
                products = await conn.fetch(query, product_id)
                logging.debug(products)
                buttons_text = [cat['name'] for cat in products]
                description_text = [cat['description'] for cat in products]
                photo_url = [cat['image_absolute_path'] for cat in products]
                price = [cat['price'] for cat in products]
                id = [cat['id'] for cat in products]
                return buttons_text, id, description_text, photo_url, price
            except Exception as _ex:
                logging.debug(_ex)

    async def get_product_by_cart(self, cart_id: int):
        async with self.pool.acquire() as conn:
            try:
                query = f"SELECT * FROM catalog_product WHERE product_id = $1"
                products = await conn.fetch(query, )
                logging.debug(products)
                buttons_text = [cat['name'] for cat in products]
                description_text = [cat['description'] for cat in products]
                photo_url = [cat['image_absolute_path'] for cat in products]
                price = [cat['price'] for cat in products]
                id = [cat['id'] for cat in products]
                return [buttons_text, id, description_text, photo_url, price]
            except Exception as _ex:
                logging.debug(_ex)

    async def add_product_to_cart(self, telegram_id, quantity, product_id):
        cart_id = await self.get_users_cart(telegram_id)
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO orders_cartitem (cart_id, product_id, quantity)
                VALUES ($1, $2, $3)
                """,
                cart_id, product_id, quantity
            )
            logging.debug('Success')

    async def get_users_cart(self, telegram_id):
        async with self.pool.acquire() as connection:
            user_id = await connection.fetchval(
                """
                SELECT id FROM users_telegramuser WHERE telegram_user_id = $1
                """,
                telegram_id
            )

            cart_id = await connection.fetchval(
                """
                SELECT id FROM orders_cart WHERE user_id = $1
                """,
                user_id
            )
            logging.debug(cart_id)
            return cart_id

    async def get_cart_items(self, telegram_id):
        cart_id = await self.get_users_cart(telegram_id)
        async with self.pool.acquire() as connection:
            cart_items = await connection.fetch(
                """
                SELECT * FROM orders_cartitem WHERE cart_id = $1
                """,
                cart_id
            )

            items_details = []
            for item in cart_items:
                product = await connection.fetchrow(
                    """
                    SELECT id, name, price, description, image_absolute_path
                    FROM catalog_product
                    WHERE id = $1
                    """,
                    item['product_id']
                )

                items_details.append({
                    'cart_item_id': item['id'],
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'product_price': product['price'],
                    'product_description': product['description'],
                    'product_image_absolute_path': product['image_absolute_path'],
                    'quantity': item['quantity']
                })

        return items_details

    async def get_cart_item(self,cart_item_id):
        async with self.pool.acquire() as connection:
            cart_items = await connection.fetch(
                """
                SELECT * FROM orders_cartitem WHERE id = $1
                """,
                cart_item_id
            )

            items_details = []
            for item in cart_items:
                product = await connection.fetchrow(
                    """
                    SELECT id, name, price, description, image_absolute_path
                    FROM catalog_product
                    WHERE id = $1
                    """,
                    item['product_id']
                )

                items_details.append({
                    'cart_item_id': item['id'],
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'product_price': product['price'],
                    'product_description': product['description'],
                    'product_image_absolute_path': product['image_absolute_path'],
                    'quantity': item['quantity']
                })

        return items_details

    async def delete_item_from_cart(self, cart_item_id):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(
                        """
                        DELETE FROM orders_cartitem
                        WHERE id = $1
                        """,
                        cart_item_id,
                    )
                    logging.debug('Успешно')
                except Exception as _ex:
                    logging.debug(_ex)

    async def delete_all_items_from_cart(self,telegram_id):
        cart_id = await self.get_users_cart(telegram_id)
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(
                        """
                        DELETE FROM orders_cartitem
                        WHERE cart_id = $1
                        """,
                        cart_id,
                    )
                    logging.debug('Успешно')
                except Exception as _ex:
                    logging.debug(_ex)

    async def change_item_from_cart(self, new_quantity, cart_item_id):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(
                        """
                        UPDATE orders_cartitem
                        SET quantity = $1
                        WHERE id = $2
                        """,
                        new_quantity,
                        cart_item_id,
                    )
                    logging.debug('Успешно')
                except Exception as _ex:
                    logging.debug(_ex)



    async def create_order(self, telegram_id):
        # Получаем список товаров из корзины
        cart_items = await self.get_cart_items(telegram_id)
        # Получаем текущий адрес пользователя
        address = await self.get_users_address(telegram_id)

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    # Получаем ID пользователя по telegram_id
                    user_id = await connection.fetchval(
                        """
                        SELECT id FROM users_telegramuser WHERE telegram_user_id = $1
                        """,
                        telegram_id
                    )

                    # Создаем заказ и получаем его ID
                    order_id = await connection.fetchval(
                        """
                        INSERT INTO orders_order (status, created_at, user_id)
                        VALUES ($1, $2, $3)
                        RETURNING id
                        """,
                        'pending', datetime.now(), user_id
                    )

                    # Добавляем товары в заказ
                    for item in cart_items:
                        product_id = item['product_id']
                        quantity = item['quantity']
                        await connection.execute(
                            """
                            INSERT INTO orders_orderitem (order_id, product_id, quantity)
                            VALUES ($1, $2, $3)
                            """,
                            order_id, product_id, quantity
                        )

                    # Добавляем адрес в заказ
                    await connection.execute(
                        """
                        INSERT INTO orders_orderaddress (order_id, city, street, house, apartment, user_id)
                        VALUES ($1, $2, $3, $4, $5, $6)
                        """,
                        order_id,
                        address['city'],
                        address['street'],
                        address['house'],
                        address['apartment'],
                        user_id
                    )

                    logging.info(f"Заказ #{order_id} успешно создан для пользователя {telegram_id}.")
                    return order_id
                except Exception as _ex:
                    logging.error(f"Ошибка при создании заказа для пользователя {telegram_id}: {_ex}")
                    raise

    async def change_order_status(self, order_id):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(
                        """
                        UPDATE orders_order
                        SET status = $1
                        WHERE id = $2
                        """,
                        'paid',
                        order_id,
                    )
                    logging.debug('Успешно')
                except Exception as _ex:
                    logging.debug(_ex)

    async def get_faq(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    logging.debug("Executing SELECT name, answer FROM faq_faq")
                    rows = await connection.fetch("SELECT name, answer FROM faq_faq")
                    logging.debug(f"Fetched rows: {rows}")
                    return {row['name']: row['answer'] for row in rows}
                except Exception as _ex:
                    logging.debug(_ex)

    async def close_pool(self):
        """Закрытие пула соединений."""
        if self.pool:
            await self.pool.close()
            logging.info("Pool closed")
