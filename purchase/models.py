from django.db import models

from product.models import ProductDetail

# Create your models here.
class DetailPurchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    detail_product_id = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)