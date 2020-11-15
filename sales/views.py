from user.views import *

from user.models import User
from sales.models import ShoppingCart, SellDeatil, StatusSell, Sell
from sales.serializers import SaleSerializer, ConfirmSaleSerializer
from product.models import ProductDetail

@api_view(['GET'])
@transaction.atomic()
@permission_classes([IsAuthenticated])
def shopping_car(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        shopping_car_user = ShoppingCart.objects.get(user_id=user, canceled=False, finish=False)
    except ShoppingCart.DoesNotExist:
        shopping_car_user = None
    if shopping_car_user is None:
        shopping_car_user = ShoppingCart.objects.create(
            quantity=0,
            user_id=user,
            sub_total=0.0,
            canceled=False,
            finish=False
        )
    sale_details = SellDeatil.objects.all().filter(shopping_cart_id=shopping_car_user)
    sales_list = []
    for sale in sale_details:
        simple_sail = {
            'quantity': sale.quantity,
            'sub_total': sale.sub_total,
            'price': sale.product_detail.price,
            'product_detail': {
                'name': sale.product_detail.product_id.name,
                'image': sale.product_detail.product_id.image,
                'brand': sale.product_detail.product_id.brand,
                'code': sale.product_detail.product_id.code,
                'size': sale.product_detail.size_id.size,
                'color': sale.product_detail.color_id.color,
            }
        }
        sales_list.append(simple_sail)
    shop_car_serializer = {
        'items': sales_list,
        'car_id': shopping_car_user.pk,
        'quantity': shopping_car_user.quantity,
        'sub_total': shopping_car_user.sub_total
    }
    return Response(shop_car_serializer, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic()
@permission_classes([IsAuthenticated])
def sale(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    serializer_sale = SaleSerializer(data=request.data)
    if serializer_sale.is_valid():
        id_product_detail = serializer_sale.data['product_detail']
        quantity = serializer_sale.data['quantity']
        id_car_shopping = serializer_sale.data['shopping_cart_id']
        try:
            shopping_car_user = ShoppingCart.objects.get(pk=id_car_shopping, canceled=False, finish=False)
        except ShoppingCart.DoesNotExist:
            return Response({"error": "car shopping not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product_detail = ProductDetail.objects.get(pk=id_product_detail)
        except ProductDetail.DoesNotExist:
            return Response({"error": "product detail not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sell_detail = SellDeatil.objects.get(product_detail=product_detail, shopping_cart_id=shopping_car_user)
        except SellDeatil.DoesNotExist:
            sell_detail = None
        if sell_detail is None:
            if product_detail.quantity < quantity:
                return Response({"error": "insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
            sub_total = quantity * product_detail.price
            SellDeatil.objects.create(
                product_detail=product_detail,
                shopping_cart_id=shopping_car_user,
                quantity=quantity,
                sub_total=sub_total
            )
        if sell_detail is not None:
            quantity = quantity + sell_detail.quantity
            if product_detail.quantity < quantity:
                return Response({"error": "insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
            sub_total = quantity * product_detail.price
            sell_detail.quantity = quantity
            sell_detail.sub_total = sub_total
            sell_detail.save()
        sell_details = SellDeatil.objects.all().filter(shopping_cart_id=shopping_car_user)
        quantity = 0
        sub_total = 0
        for sell in sell_details:
            quantity = quantity + sell.quantity
            sub_total = sub_total + sell.sub_total
        shopping_car_user.quantity = quantity
        shopping_car_user.sub_total = sub_total
        shopping_car_user.save()
        return Response({"response": "ok"}, status=status.HTTP_200_OK)
    return Response(serializer_sale.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@transaction.atomic()
@permission_classes([IsAuthenticated])
def make_sale(request, id):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ConfirmSaleSerializer(data=request.data)
    if serializer.is_valid():
        try:
            shopping_cart = ShoppingCart.objects.get(pk=id, canceled=0, finish=0)
        except ShoppingCart.DoesNotExist:
            return Response({"error": "cart not found"}, status=status.HTTP_400_BAD_REQUEST)
        details_sale = SellDeatil.objects.all().filter(shopping_cart_id=shopping_cart)
        sid = transaction.savepoint()
        for details_sale in details_sale:
            quantity_car = details_sale.quantity
            product_detail_cart = details_sale.product_detail
            quantity_stock = product_detail_cart.quantity
            if quantity_car > quantity_stock:
                transaction.savepoint_rollback(sid)
                return Response({"error": "insufficient stock ",
                                 "message": {
                                     "product": details_sale.product_detail.product_id.name,
                                     "code":details_sale.product_detail.product_id.code,
                                     "category": details_sale.product_detail.product_id.category,
                                     "brand":  details_sale.product_detail.product_id.brand,
                                     "color": details_sale.product_detail.color_id.color,
                                     "size": details_sale.product_detail.size_id.size,

                                 }}
                                , status=status.HTTP_400_BAD_REQUEST)
            product_detail_cart.quantity = product_detail_cart.quantity - quantity_car
            product = product_detail_cart.product_id
            product.quantity = product.quantity - quantity_car
            product.save()
            product_detail_cart.save()
        shopping_cart.finish = True
        shopping_cart.save()
        sell_finish = Sell.objects.create(
            shopping_car_id=shopping_cart,
            address=serializer.data['address'],
            method_pay=serializer.data['method_pay'],
        )
        StatusSell.objects.create(
            state=1,
            code="random code",
            sell_id=sell_finish
        )
        return Response({"response":"ok"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)