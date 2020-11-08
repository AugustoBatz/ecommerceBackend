"""ecommerceBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from user import views as user_view
from product import views as product_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user', user_view.user_list),
    path('api/user/product', product_view.get_products_for_user),
    path('api/user/product/detail/<str:code>', product_view.get_products_detail_for_user),
    path('api/user/profile', user_view.profile),
    path('api/signup', user_view.user_signup),
    path('api/login', user_view.authenticate_user),
    path('api/recover', user_view.request_new_password),
    path('api/login/admin', user_view.authenticate_admin),
    path('api/product', product_view.productoAPIView.as_view()),
    path('api/product/<str:code>/', product_view.productoEspecificoAPIView.as_view()),
    path('api/product/detail', product_view.add_product_detail),
    path('api/product/detail/purchase', product_view.add_product_detail_purchase),
    path('api/product/sub-detail/<str:code>', product_view.get_products_detail),
    path('api/product/listsubproducts', product_view.get_all_products_detail),
    path('api/product/search/<str:search>/', product_view.search_products)   
]
