from __future__ import absolute_import ,unicode_literals
from celery import Celery
from django.conf import settings
import os

#settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE","pricetracker.settings")

app = Celery("pricetracker")
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kathmandu')
app.config_from_object('django.conf:settings', namespace="CELERY")

# CELERY BEAT Settings
app.conf.beat_schedule = {

}

app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')