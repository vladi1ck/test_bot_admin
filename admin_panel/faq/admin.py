from django.contrib import admin

from faq.models import FAQ


# Register your models here.
@admin.register(FAQ)
class PushAdmin(admin.ModelAdmin):
    list_display = ('name', 'answer')

