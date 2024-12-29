from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django sozlamalarini Celery uchun import qilish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Celery konfiguratsiyasini import qilish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Asinxron vazifalarni avtomatik ravishda topish
app.autodiscover_tasks()
