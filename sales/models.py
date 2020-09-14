from django.db import models

from user.models import User
from product.models import ProductDetail

# Create your models here.
class ShoppingCart(models.Model):
    quantity = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_total = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField()
    finish = models.BooleanField()

class SellDeatil(models.Model):
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.FloatField()

class Sell(models.Model):
    shopping_carg_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class StatusSell(models.Model):
    state = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=25)
    sell_id = models.ForeignKey(Sell, on_delete=models.CASCADE)