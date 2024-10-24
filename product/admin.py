from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Product, ProductImage, Category
from django.db import models as dj_models
from django.contrib.admin.widgets import AdminTextareaWidget

class ImageInline(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']
    inlines = [ImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']

    def has_module_permission(self, request: HttpRequest, obj:Any | None = ...) -> bool:
        return False