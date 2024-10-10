from django.contrib import admin
from order.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user', 'product']
    list_display_links = ['user', 'product']
    readonly_fields = ['total_price']