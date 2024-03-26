from rest_framework import status
from django.http import HttpResponse
from ..models import Product, ProductDetail, PriceHistory
from django.core.exceptions import ObjectDoesNotExist
import time
from django.contrib.auth.models import User
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Scrape:
    def __init__(self):
        pass
    def scrape(self):
        try:
            urls = Product.objects.all()
        except:
            return "No Url Found"
        
        for  product in urls:
            url = product.url
            id = product.id

            #start scraping
            data = self.scrape_data(url)
            title = data[0]
            price = int(data[1])
            description= data[2]

            product_details = ProductDetail.objects.filter(product_id=id)
            if not product_details:
                detail = ProductDetail(product_id=id,name = title, description= description)
                detail.save()
                print('new detail updated.')
            else:
                print('details are upto date.')
            
            try:
                price_db = PriceHistory.objects.filter(last_price=price).latest('created_date')
                if price != price_db.last_price:
                    detail2 = PriceHistory(product_id=id,last_price=price)
                    detail2.save()
                    print('New price updated.')
                else:
                    print('Price is upto date.')
            except ObjectDoesNotExist:
                detail2 = PriceHistory(product_id=id,last_price=price)
                detail2.save()
                
        return  HttpResponse(f'scraping Completed',status=status.HTTP_200_OK)
      
    def scrape_data(self,url):
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