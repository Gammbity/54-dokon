import schedule
import time
from django.utils.timezone import now
import datetime


def is_new():
    from product.models import Product  # Import here to avoid early access
    checking_date = now() - datetime.timedelta(minutes=10)
    products = Product.objects.filter(is_new=True)
    for product in products:
        if product.created_at < checking_date:
            product.is_new = False
            print(product.is_new)
            product.save()

def schedule_tasks():
    # schedule.every().days.at('00:00').do(is_new)
    schedule.every(5).seconds.do(is_new)

    while True:
        schedule.run_pending()
        # time.sleep(60)
        time.sleep(1)

