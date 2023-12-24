import os
from celery import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","pricetracker.settings")
app = celery("pricetracker")
app.config_from_object('django.conf:settings', namespcae="CELERY")
app.autodiscover_tasks()
