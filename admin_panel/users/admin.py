from django.contrib import admin

from orders.models import Order, OrderItem, OrderAddress
from users.models import TelegramUser, Address



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAddressInline(admin.TabularInline):
    model = OrderAddress
    extra = 1

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    inlines = [OrderItemInline, OrderAddressInline]


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    inlines = [OrderInline, OrderAddressInline]
    list_display = ('telegram_user_id', 'last_name', 'first_name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'house')
