from django.db import models
from order.models import Order
from user.models import User
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.Model):
    method = models.CharField(max_length=20, choices=[
        ("payme", "PayMe"),
        ("click", "Click"),
        ("paynet", "Paynet")
    ], default="paynet")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.method
    
    class Meta:
        verbose_name = _("to'lov usul")
        verbose_name_plural = _("to'lov usullar")

class PaymentStatus(models.Model):
    status = models.CharField(max_length=20, choices=[
        ("success", "Success"),
        ("faile", "faile")
    ], default="success")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = _("to'lov holati")
        verbose_name_plural = _("to'lov holati")


class Payment(models.Model):
    method_id = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='method_payment')
    status_id = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, related_name='status_payment')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='')
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id.user_id.get_full_name()}-{self.order_id}"
    
    class Meta:
        verbose_name = _("To'lov")
        verbose_name_plural = _("To'lovlar")