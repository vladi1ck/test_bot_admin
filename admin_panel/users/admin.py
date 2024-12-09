from django.contrib import admin

from users.models import TelegramUser, Address


@admin.register(TelegramUser)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', 'last_name', 'first_name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'house')
