import time
from celery import shared_task
from tracker.scrape import scrape_data
from .models import Product

@shared_task
def trackprice():
    """
    get urls from the models
    """
    scrape_data('')
    return 'hello'

