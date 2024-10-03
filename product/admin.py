from django.contrib import admin
from product import models
# from modeltranslation.admin import TranslationAdmin

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']

# class ProductInline(TranslationAdmin):
#     model = models.Product
#     extra = 0
#     fields = ['name']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']
    # inlines = [ProductInline]

