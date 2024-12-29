from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Product, ProductImage, Category, Comment


class ImageInline(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']
    search_fields = ['name', 'price']
    inlines = [ImageInline]
    readonly_fields = ['with_rebate', 'slug']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']
    readonly_fields = ['slug']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    list_display_links = ['user', 'id']
    # readonly_fields = ['text', 'user', 'product']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']

    def has_module_permission(self, request: HttpRequest, obj:Any | None = ...) -> bool:
        return False