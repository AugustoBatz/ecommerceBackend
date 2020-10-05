from rest_framework import serializers
from .models import Product

class ProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'