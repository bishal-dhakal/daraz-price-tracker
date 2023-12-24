from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    desired_price = models.IntegerField(default=0)
    description= models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class PriceHistory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    last_price = models.IntegerField(default=0,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.last_price} on {self.date}"
