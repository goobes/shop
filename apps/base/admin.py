
from django.contrib import admin
from .models import Item, Profile, Payment

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']


