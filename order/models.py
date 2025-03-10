from django.db import models
from user.models import User
from product.models import Product
from django.utils.translation import gettext_lazy as _


class Basket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_basket")
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.id}"

    class Meta:
        verbose_name = _("savat")
        verbose_name_plural = _("savatlar")
        ordering = ['-created_at']

class Status(models.Model):
    status = models.CharField(max_length=20, choices=[
        ("pending", "kutishda"),
        ("shipped", "jo'natilgan"),
        ("delivered", "yetkazib berildi"),
        ("cancelled", "bekor qilingan")
    ], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 

class Address(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.location
    
    class Meta:
        verbose_name = _('Manzil')
        verbose_name_plural = _("Manzillar")

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status_order')
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_order')
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_order')
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
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order_item')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_order_item')
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.order.user.get_full_name()


    class Meta:
        verbose_name = _("Buyurtma elementi")
        verbose_name_plural = _("Buyurtma elementlari")
        ordering = ['-created_at']


class BasketItem(models.Model):
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_basket_item')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_basket_item')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.basket_id.user.get_full_name()} - {self.basket_id}"
    
    class Meta:
        verbose_name = _("Savat elementi")
        verbose_name_plural = _("Savat elementlari")