import os

from django.db import models
from django.template.context_processors import media

from admin_panel import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Category', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['id']

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    image_absolute_path = models.TextField(blank=True, null=True)  # Поле для абсолютного пути


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['id']

    def __str__(self):
        return self.name