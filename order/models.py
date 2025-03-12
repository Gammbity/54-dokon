from django.db import models
from user.models import User
from product.models import Product
from django.utils.translation import gettext_lazy as _


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets")
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.id}"
    
    def clean(self):
        self.items.all().delete()
        self.total_price = 0
        self.save()

    class Meta:
        verbose_name = _("savat")
        verbose_name_plural = _("savatlar")
        ordering = ['-created_at']

class Status(models.Model):
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = _("Holat")
        verbose_name_plural = _("Holatlar")

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='order_with_status')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='order_at_address')
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
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
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.basket.user.get_full_name()} - {self.basket}"
    
    class Meta:
        verbose_name = _("Savat elementi")
        verbose_name_plural = _("Savat elementlari")