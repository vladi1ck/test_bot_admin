from django.contrib import admin

from push_from_bot.models import Push


@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    list_display = ('text_message', 'created_at', 'sent')  # Добавим поле sent для удобства
    actions = ('send_push',) # Регистрируем метод как action

    @admin.action(description="Отправить выбранные push-уведомления")
    def send_push(self, request, queryset):
        for broadcast in queryset.filter(sent=False):  # Только неотправленные сообщения
            from push_from_bot.tasks import send_broadcast_message
            send_broadcast_message.delay(broadcast.id)
        self.message_user(request, "Сообщения добавлены в очередь на отправку.")  # Сообщение об успехе
    send_push.short_description = "Отправить выбранные push-уведомления"  # Имя для кнопки в интерфейсе