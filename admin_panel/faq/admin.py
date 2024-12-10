from django.contrib import admin

from faq.models import FAQ


@admin.register(FAQ)
class PushAdmin(admin.ModelAdmin):
    list_display = ('name', 'answer')

