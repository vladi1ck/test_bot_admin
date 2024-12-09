from django.contrib import admin

from catalog.models import Category, Product, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(SubCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
