from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    address_a = models.CharField(max_length=45)
    address_b = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
