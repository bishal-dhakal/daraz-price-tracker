from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task
from urllib.request import Request
from .models import Product
import logging

logger = logging.getLogger(__name__)

@shared_task
def add(x,y):
    print(f'total sum = {x+y}')
    result = x + y
    logger.info(f'Total sum: {result}')
    return x+y
