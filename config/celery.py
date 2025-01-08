from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Django sozlamalarini Celery uchun import qilish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Celery konfiguratsiyasini import qilish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Asinxron vazifalarni avtomatik ravishda topish
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-delete-passwords-every-week': {
        'task': 'user.tasks.delete_passwords',
        'schedule': crontab(
            minute=0,
            hour=0,
            day_of_week='sunday'
        ),
    },
    'run-is-new-every-week': {
        'task': 'product.tasks.is_new',
        'schedule': crontab(
            minute=0,
            hour=0,
            day_of_week='sunday'
        ),
    },
}