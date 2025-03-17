from django.contrib import admin
from order.models import Order, Basket, OrderItem, Address, Status, BasketItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user']
    list_display_links = ['user']
    readonly_fields = ['total_price']

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_link = ['id']
    readonly_fields = ['price']

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    list_display_link = ['user']
    readonly_fields = ['total_price']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'location']
    list_display_link = ['id', 'location']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_display_link = ['id', 'status']

@admin.register(OrderItem)
class OrerItemtAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'id']
    list_display_link = ['order', 'product']
    readonly_fields = ['order', 'product', 'price', 'quantity']