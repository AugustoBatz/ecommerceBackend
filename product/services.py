from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from product.models import Product, Color, Size, ProductDetail


def create_detail_product(serializer):
    try:
        product = Product.objects.get(code=serializer.data['code_product'])
    except Product.DoesNotExist:
        return Response({
            'code': 400,
            'description': 'El producto no existe'
        }, status=status.HTTP_404_NOT_FOUND)
    try:
        color = Color.objects.get(color=serializer.data['color'])
    except Color.DoesNotExist:
        color = Color.objects.create(color=serializer.data['color'])
    try:
        size = Size.objects.get(size=serializer.data['size'])
    except Size.DoesNotExist:
        size = Size.objects.create(size=serializer.data['size'])

    try:
        product_detail = ProductDetail.objects.create(
            product_id=product,
            size_id=size,
            color_id=color,
            quantity=0,
            price=serializer.data['price']
        )
        data = {
            'product': product.code,
            'size': product_detail.size_id.size,
            'color': product_detail.color_id.color,
            'quantity': product_detail.quantity,
            'price': product_detail.price
        }
        return Response(data, status=status.HTTP_200_OK)
    except IntegrityError as e:
        return Response({
            'code': 400,
            'description': 'Este detalle ya existe'
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
