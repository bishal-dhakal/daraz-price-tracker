from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task
import logging
from .Utils.Scraper import Scrape
import time

logger = logging.getLogger(__name__)

@shared_task
def cel_scraper():
    scraper= Scrape()
    scraper.scrape()

#TODO : destory task after 10 min whatver the status performed or not