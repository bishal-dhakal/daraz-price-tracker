from ..models import *
from django.db.models import F,Max
from django.core.mail import send_mail
from django.utils.html import strip_tags
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self) -> None:
        pass

    def email(self):
        latest_prices_per_user = PriceHistory.objects.values(
            'product__user__email'
        ).annotate(
            latest_date=Max('created_date')
        ).filter(
            created_date=F("latest_date")
        ).values(
            'product__user__email', 
            'product__productdetail__name', 
            'product__desired_price', 
            price=F('last_price'),
        )

        email_content = "<h2>Latest Prices from Price Tracker</h2>"
        email_content += "<table border='1'><tr><th>User Email</th><th>Product Name</th><th>Desired Price</th><th>Last Price</th></tr>"

        for price_info in latest_prices_per_user:
            user_email = price_info['product__user__email']
            product_name = price_info['product__productdetail__name']
            desired_price = price_info['product__desired_price']
            last_price = price_info['price']


        if desired_price >= last_price:
            email_content += f"<tr><td>{user_email}</td><td>{product_name}</td><td>{desired_price}</td><td>{last_price}</td></tr>"

            email_content += "</table>"

            subject = "Latest Prices Update"
            html_message = email_content
            plain_message = strip_tags(html_message)
            from_email = 'jethalalgada1902@gmail.com'
            to_emails = [user['product__user__email'] for user in latest_prices_per_user]
            print(to_emails)
            send_mail(subject, plain_message, from_email, to_emails,fail_silently=True, html_message=html_message)

        return "task executed - email sent"