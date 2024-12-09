from django.db import models

class Push(models.Model):
    text_message = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['id']

    def __str__(self):
        return self.text_message