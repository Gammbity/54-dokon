from django.contrib import admin
from order.models import Order, Basket, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user']
    list_display_links = ['user']
    readonly_fields = ['user', 'total_price', 'longitude', 'latitude', 'location']

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'id']
    list_display_link = ['user', 'product']

@admin.register(OrderItem)
class OrerItemtAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'id']
    list_display_link = ['order', 'product']
    readonly_fields = ['order', 'product', 'price', 'quantity']