from django.contrib import admin

from push_from_bot.models import Push


@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    list_display = ('text_message', 'created_at', 'sent')
    actions = ('send_push',)

    @admin.action(description="Отправить выбранные push-уведомления")
    def send_push(self, request, queryset):
        for broadcast in queryset.filter(sent=False):
            from push_from_bot.tasks import send_broadcast_message
            send_broadcast_message.delay(broadcast.id)
        self.message_user(request, "Сообщения добавлены в очередь на отправку.")
    send_push.short_description = "Отправить выбранные push-уведомления"