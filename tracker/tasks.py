from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task
import logging
from .Utils.Scraper import Scrape
from .Utils.notifier import EmailNotifier

logger = logging.getLogger(__name__)


@shared_task
def cel_scraper():
    scraper = Scrape()
    scraper.scrape()

@shared_task
def cel_email():
    email = EmailNotifier()
    email.email()