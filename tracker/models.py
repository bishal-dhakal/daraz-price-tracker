from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext as _

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __Str__(self):
        return  self.email


class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    desired_price = models.IntegerField(default=0)

    def __str__(self):
        return self.url


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=1000, default=None)

    # slug = models.CharField(max_length=200, default=None, index=True)

    def __str__(self):
        return self.name


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    last_price = models.IntegerField(default=0, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.product.url} - {self.last_price} on {self.date}"
