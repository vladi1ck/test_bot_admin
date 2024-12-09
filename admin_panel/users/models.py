from django.db import models

class TelegramUser(models.Model):
    telegram_user_id = models.BigIntegerField(null=False, blank=False, db_index=True, unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = 'Пользователь Телеграма'
        verbose_name_plural = 'Пользователи Телеграма'
        ordering = ['id']

    def __str__(self):
        return str(self.telegram_user_id)

class Address(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, null=False, blank=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    house = models.CharField(max_length=255, null=False, blank=False)
    apartment = models.CharField(max_length=255, null=True, blank=False)
