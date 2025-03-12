from django.contrib import admin
from payment import models

@admin.register(models.PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id', "method"]
    list_display_links = ['id', "method"]

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']

