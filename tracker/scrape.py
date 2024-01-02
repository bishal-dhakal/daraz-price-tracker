from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from .models import ProductDetail,PriceHistory
import time
import sys


def scrape_data(url):
    user_agent = "Mozilla/5.0"
    options = webdriver.EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument('user-agent={0}'.format(user_agent))
    browser = webdriver.Edge(options=options)
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    desired_class = 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'
    # Find the element with the specified class
    price = soup.find('span', class_=desired_class).get_text()
    price =price.replace(',','').removeprefix('Rs. ')
    title = soup.find('span',class_="pdp-mod-product-badge-title").get_text()
    description = soup.find('div',class_="html-content pdp-product-highlights").get_text()
    browser.quit()
    return title,price,description


