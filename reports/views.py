
from user.views import *

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from sales.models import Sell, SellDeatil, ShoppingCart
import datetime


@api_view(['GET'])
@transaction.atomic()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_sales(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    date_start_param = request.GET.getlist("date_start")
    date_finish_param = request.GET.getlist("date_finish")
    current_date_and_time = datetime.datetime.now()
    hour = current_date_and_time.hour
    minute = current_date_and_time.minute
    second = current_date_and_time.second
    date_time_start = datetime.datetime.strptime(date_start_param[0], '%Y-%m-%d')
    date_time_finish = datetime.datetime.strptime(date_finish_param[0], '%Y-%m-%d')
    date_time_start = date_time_start.replace(hour=hour, minute=minute, second=second)
    date_time_finish = date_time_finish.replace(hour=hour, minute=minute, second=second)
    print(date_time_start)
    print(date_time_finish)
    sales = Sell.objects.all().filter(date__range=(date_time_start, date_time_finish))
    sales_report = []
    for sale in sales:
        sale_details_data = []
        sale_details = SellDeatil.objects.all().filter(shopping_cart_id=sale.shopping_car_id)
        for sale_detail in sale_details:
            sale_detail_data = {
                "product": sale_detail.product_detail.product_id.name,
                "code": sale_detail.product_detail.product_id.code,
                "category": sale_detail.product_detail.product_id.category,
                "brand": sale_detail.product_detail.product_id.brand,
                "details": {
                    "size": sale_detail.product_detail.size_id.size,
                    "color": sale_detail.product_detail.color_id.color,
                    "quantity": sale_detail.quantity,
                    "sub_total": sale_detail.sub_total,
                    "price": sale_detail.product_detail.price
                }

            }
            sale_details_data.append(sale_detail_data)
        sale_report = {
            "date": sale.date,
            "address": sale.address,
            "user": sale.shopping_car_id.user_id.username,
            "total": sale.shopping_car_id.sub_total,
            "quantity": sale.shopping_car_id.quantity,
            "sale_detail": sale_details_data

        }
        sales_report.append(sale_report)
    return Response(sales_report, status=status.HTTP_200_OK)


@api_view(['GET'])
@transaction.atomic()
@permission_classes([IsAuthenticated])
def get_sales_by_user(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    date_start_param = request.GET.getlist("date_start")
    date_finish_param = request.GET.getlist("date_finish")
    current_date_and_time = datetime.datetime.now()
    hour = current_date_and_time.hour
    minute = current_date_and_time.minute
    second = current_date_and_time.second
    date_time_start = datetime.datetime.strptime(date_start_param[0], '%Y-%m-%d')
    date_time_finish = datetime.datetime.strptime(date_finish_param[0], '%Y-%m-%d')
    date_time_start = date_time_start.replace(hour=hour, minute=minute, second=second)
    date_time_finish = date_time_finish.replace(hour=hour, minute=minute, second=second)
    print(date_time_start)
    print(date_time_finish)
    sales = Sell.objects.all().filter(shopping_car_id__user_id=user, date__range=(date_time_start, date_time_finish))
    sales_report = []
    for sale in sales:
        sale_details_data = []
        sale_details = SellDeatil.objects.all().filter(shopping_cart_id=sale.shopping_car_id)
        for sale_detail in sale_details:
            sale_detail_data = {
                "product": sale_detail.product_detail.product_id.name,
                "code": sale_detail.product_detail.product_id.code,
                "category": sale_detail.product_detail.product_id.category,
                "brand": sale_detail.product_detail.product_id.brand,
                "details": {
                    "size": sale_detail.product_detail.size_id.size,
                    "color": sale_detail.product_detail.color_id.color,
                    "quantity": sale_detail.quantity,
                    "sub_total": sale_detail.sub_total,
                    "price": sale_detail.product_detail.price
                }

            }
            sale_details_data.append(sale_detail_data)
        sale_report = {
            "date": sale.date,
            "address": sale.address,
            "total": sale.shopping_car_id.sub_total,
            "quantity": sale.shopping_car_id.quantity,
            "sale_detail": sale_details_data

        }
        sales_report.append(sale_report)
    return Response(sales_report, status=status.HTTP_200_OK)