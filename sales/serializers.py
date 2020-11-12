from rest_framework import serializers


class SaleSerializer(serializers.Serializer):
    product_detail = serializers.IntegerField()
    quantity = serializers.IntegerField()
    shopping_cart_id = serializers.IntegerField()