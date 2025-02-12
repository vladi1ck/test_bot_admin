from django.db import models

from users.models import TelegramUser


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
    ]

    user = models.ForeignKey('users.TelegramUser', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']

    def __str__(self):
        return f'Заказ от {self.created_at}'

class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="address")
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE,  related_name="address_user")
    city = models.CharField(max_length=255, null=False, blank=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    house = models.CharField(max_length=255, null=False, blank=False)
    apartment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес Заказа'
        verbose_name_plural = 'Адреса Заказов'
        ordering = ['id']

    def __str__(self):
        return f'{self.order}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Итем заказа'
        verbose_name_plural = 'Итемы заказов'
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Cart(models.Model):
    user = models.ForeignKey('users.TelegramUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_cart')
        ]

    def __str__(self):
        return f"Cart of {str(self.user)}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"