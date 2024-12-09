from django.apps import AppConfig

class PushFromBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'push_from_bot'

    def ready(self):
        import push_from_bot.signals
