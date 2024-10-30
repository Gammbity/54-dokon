from django.contrib import admin
from order.models import Order, Basket, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user']
    list_display_links = ['user']
    readonly_fields = ['total_price']

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'id']
    list_display_link = ['user', 'product']

@admin.register(OrderItem)
class OrerItemtAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'id']
    list_display_link = ['order', 'product']