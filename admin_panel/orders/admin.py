from django.contrib import admin

from orders.models import Order, Cart, CartItem, OrderAddress, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')

@admin.register(OrderAddress)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
