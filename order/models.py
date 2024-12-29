from django.db import models
from user.models import User
from product.models import Product
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ("pending", "kutishda"),
        ("shipped", "jo'natilgan"),
        ("delivered", "yetkazib berildi"),
        ("cancelled", "bekor qilingan")
    ], default="pending")
    total_price = models.PositiveBigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("buyurtma")
        verbose_name_plural = _("buyurtmalar")
        ordering = ['-created_at']


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.order.user.get_full_name()

    # https://github.com/ozodbekAI/StoreAPI/blob/main/products/views.py

    class Meta:
        verbose_name = _("Buyurtma elementi")
        verbose_name_plural = _("Buyurtma elementlari")
        ordering = ['-created_at']


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("savat")
        verbose_name_plural = _("savatlar")
        ordering = ['-created_at']
