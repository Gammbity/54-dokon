from django.db import models
from order.models import Order, Status
from user.models import User
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.Model):
    method = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.method
    
    class Meta:
        verbose_name = _("to'lov usul")
        verbose_name_plural = _("to'lov usullar")


class Payment(models.Model):
    method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT, related_name='method_payment')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status_payment')
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name='payment')
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.user.get_full_name()}-{self.order}"
    
    class Meta:
        verbose_name = _("To'lov")
        verbose_name_plural = _("To'lovlar")