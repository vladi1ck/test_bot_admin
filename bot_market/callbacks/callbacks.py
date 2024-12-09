from aiogram.filters.callback_data import CallbackData


class CategoryCbData(CallbackData, prefix="cat"):
    name: str
    id: int


class SubCategoryCbData(CallbackData, prefix="sub"):
    name: str
    id: int


class ProductCbData(CallbackData, prefix="prod"):
    name: str
    # id: int


class ProductToCart(CallbackData, prefix='to_cart', sep=';'):
    name: str
    price: float
    id: int
    description: str


class ProductToCartQuantity(CallbackData, prefix='quantity', sep=';'):
    name: str
    price: float
    id: int
    command:int
    quantity: int=0


class ProductToCartQuantityConfirmation(CallbackData, prefix='confirm_cart', sep=';'):
    id:int
    quantity: int


class ProductToCartQuantityConfirmationDone(CallbackData, prefix='confirm_done', sep=';'):
    id: int


class CategoryPageCbData(CallbackData, prefix="cat_page"):
    number: int


class SubCategoryPageCbData(CallbackData, prefix="sub_page"):
    number: int
    name: str


class ProductPageCbData(CallbackData, prefix="prod_page"):
    number: int
    id: int


class CartPageCbData(CallbackData, prefix="cart_page"):
    number: int


class BackToMenu(CallbackData, prefix="back_to_menu"):
    name: str


class CartDeleteItem(CallbackData, prefix="delete_item_from_cart"):
    cart_item_id: int


class CartChangeItem(CallbackData, prefix="change_item_from_cart"):
    cart_item_id: int

class CartChangeItemConfirm(CallbackData, prefix="confirm_change_item_from_cart"):
    cart_item_id: int
    quantity: int


class ChangeProductToCartQuantity(CallbackData, prefix="quantity_change_item_from_cart"):
    cart_item_id: int
    command:int
    quantity:int


class DeleteAllItemsFromCart(CallbackData, prefix="delete_all_items_from_cart"):
    cart_item_id: int


class CartConfirmOrder(CallbackData, prefix="cart_confirm"):
    sum: int


class Payments(CallbackData, prefix="payments"):
    sum: int
