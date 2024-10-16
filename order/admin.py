from django.contrib import admin
from order.models import Order, Basket

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user', 'product']
    list_display_links = ['user', 'product']
    readonly_fields = ['total_price']

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'id']
    list_display_link = ['user', 'product']