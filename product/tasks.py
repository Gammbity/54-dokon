from celery import shared_task
from product.models import Product
from datetime import datetime, timedelta


@shared_task
def is_new():
    day = datetime.now() - timedelta(days=7)
    Product.objects.filter(created_at__lte=day).update(is_new=False)
