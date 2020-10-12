from rest_framework import serializers
from .models import Product


class ProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductoModificacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand']
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.nombre)
        instance.category = validated_data.get('category', instance.category)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.save()
        return instance


class ProductDetailSerializer(serializers.Serializer):
    code_product = serializers.CharField(required=True, allow_blank=True, max_length=100)
    color = serializers.CharField(required=True, allow_blank=True, max_length=100)
    size = serializers.CharField(required=True, allow_blank=True, max_length=100)
    price = serializers.FloatField(required=True)
