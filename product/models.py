from django.db import ConnectionHandler, models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=25)
    brand = models.CharField(max_length=25)
    image = models.TextField()
    quantity = models.IntegerField()

class Color(models.Model):
    color = models.CharField(max_length=15)
    
class Size(models.Model):
    size = models.CharField(max_length=15)

class ProductDetail(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_id = models.ForeignKey(Size, on_delete=models.CASCADE)
    color_id = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    class Meta:
        unique_together = ('product_id', 'size_id', 'color_id')

class PurchaseDetail(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    cost = models.FloatField()
    detail_product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)