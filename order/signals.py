from django.db.models.signals import post_save
from django.dispatch import receiver
from order.models import Order

@receiver(post_save, sender=Order)
def total_price(sender, created, instance, **kwargs):
    if created:
        instance.total_price = instance.product.price * instance.quantity
        instance.save()