from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from product.models import Product, Color, Size, ProductDetail, PurchaseDetail
from django.db.models import Q

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
            "id": product_detail.pk,
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


def create_detail_purchase_product(serializer):
    try:
        detail_product = ProductDetail.objects.get(pk=serializer.data['id_detail_product'])
        product = detail_product.product_id
    except ProductDetail.DoesNotExist:
        return Response({
            'code': 404,
            'description': 'El Detalle del producto no existe'
        }, status=status.HTTP_404_NOT_FOUND)

    product_detail_purchase = PurchaseDetail.objects.create(
        detail_product=detail_product,
        quantity=serializer.data['quantity'],
        cost=serializer.data['cost']
    )
    detail_product.quantity = detail_product.quantity + product_detail_purchase.quantity
    detail_product.save()
    product.quantity = product.quantity + product_detail_purchase.quantity
    product.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_sub_details_product(code):
    try:
        product = Product.objects.get(code=code)
    except Product.DoesNotExist:
        return Response({
            'code': 404,
            'description': 'El producto no existe'
        }, status=status.HTTP_404_NOT_FOUND)
    products_details = ProductDetail.objects.filter(product_id=product.pk)
    details = []
    total = 0
    for product_detail in products_details:
        detail = {
            "size": product_detail.size_id.size,
            "color": product_detail.color_id.color,
            "quantity": product_detail.quantity,
            "price": product_detail.price,
            "id": product_detail.pk
        }
        total = total + product_detail.quantity
        details.append(detail)
    data = {
        "stock": total,
        "name": product.name,
        "code": product.code,
        "category": product.category,
        "brand": product.brand,
        "details": details,
    }
    return Response(data, status=status.HTTP_200_OK)

def get_all_details():
    try:
        allproducts = Product.objects.all()
        list_of_subproducts = []
        for i in allproducts:
           
            products_details = ProductDetail.objects.filter(product_id=i.pk)
            details = []
            total = 0
            for product_detail in products_details:
                detail = {
                    "size": product_detail.size_id.size,
                    "color": product_detail.color_id.color,
                    "quantity": product_detail.quantity,
                    "price": product_detail.price,
                    "id": product_detail.pk
                }
                total = total + product_detail.quantity
                details.append(detail)
            sub_ = {
                'id': i.id,
                'name': i.name,
                'code': i.code,
                'category': i.category,
                'brand': i.brand,
                'image': i.image,
                'subproducts': details
            }

            list_of_subproducts.append(sub_)
        for item in list_of_subproducts:
            print(item)
        return Response(list_of_subproducts, status=status.HTTP_202_ACCEPTED)
    except Product.DoesNotExist:
        return Response({
            'code': 404,
            'description': 'Error al mostrar todos los subproductos'
        }, status=status.HTTP_404_NOT_FOUND)

def get_search(search):
    try:
        p_found = True
        b_found = True
        products_p_found = Product.objects.filter(name__icontains=search)
        brand_p_found = Product.objects.filter(brand__icontains=search)
        if not products_p_found:
            p_found = False

        if not brand_p_found:
            b_found = False

        if b_found and p_found:

            products_found =  Product.objects.filter(Q(name__icontains=search) | Q(brand__icontains=search))
        if p_found == False and b_found == True:

            products_found = Product.objects.filter(brand__icontains=search)
        if p_found == True and b_found == False:

            products_found = Product.objects.filter(name__icontains=search)
        if p_found == False and b_found == False:
            return Response({
                'code': 404,
                'description': 'Error al mostrar todos los subproductos'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(get_products_found(products_found), status=status.HTTP_404_NOT_FOUND)

    except Product.DoesNotExist:
        return Response({
            'code': 404,
            'description': 'Error al mostrar todos los subproductos'
        }, status=status.HTTP_404_NOT_FOUND)

def get_products_found(list_objects):
    ret = []
    for i in list_objects:
        try:
            product = Product.objects.get(code=i.code)
        except Product.DoesNotExist:
            return null
        products_details = ProductDetail.objects.filter(product_id=product.pk)
        details = []
        total = 0
        for product_detail in products_details:
            detail = {
                "size": product_detail.size_id.size,
                "color": product_detail.color_id.color,
                "quantity": product_detail.quantity,
                "price": product_detail.price,
                "id": product_detail.pk
            }
            total = total + product_detail.quantity
            details.append(detail)
        data = {
            "stock": total,
            "name": product.name,
            "code": product.code,
            "category": product.category,
            "brand": product.brand,
            "details": details,
        }
        ret.append(data)
    return ret




def get_products_user():
    products = Product.objects.all().filter(quantity__gte=0)
    products_list = []
    for product in products:
        if product.quantity != 0:
            simple_product = {
                "code": product.code,
                "name": product.name,
                "category": product.category,
                "brand": product.brand,
                "image": product.image,
                "stock": product.quantity
            }
            products_list.append(simple_product)
    return Response(products_list, status=status.HTTP_200_OK)