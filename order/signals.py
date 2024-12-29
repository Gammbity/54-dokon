from django.db.models.signals import post_save
from django.dispatch import receiver
from order.models import Order
from bot.order_bot import bot_order, bot
import asyncio

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        raise

@receiver(post_save, sender=Order)
def order_save(sender, instance, created, **kwargs):
    if created:
        try:
            loop = get_or_create_eventloop()
            loop.run_until_complete(bot_order(instance.user, bot))
        except Exception as e:
            print(f"Error in async execution: {e}")