from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    desired_price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.url
    
class ProductDetail(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=None)
    description= models.CharField(max_length=1000, default=None)
    # slug = models.CharField(max_length=200, default=None, index=True)

    def __str__(self):
        return self.name

    
class PriceHistory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    last_price = models.IntegerField(default=0,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.product.url} - {self.last_price} on {self.date}"
