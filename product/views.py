from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .serializers import ProductoSerializers, ProductDetailSerializer, ProductDetailPurchaseSerializer
from django.http import Http404
from user.views import *
from product.services import *


class productoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    """
    Ingresa un producto
    """

    def post(self, request):
        serializer = ProductoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Obtiene la lista de productos
    """

    def get(self, request):
        productos = Product.objects.all()
        serializer = ProductoSerializers(productos, many=True)
        return Response(serializer.data)


class productoEspecificoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    """
    Obtiene la lista de productos
    """

    def get_object(self, code):
        try:
            return Product.objects.get(code=code)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, code):
        producto = self.get_object(code)
        serializer = ProductoSerializers(producto)
        return Response(serializer.data)

    """
    Modifica un producto
    """

    def put(self, request, code):

        producto = self.get_object(code)
        serializer = ProductoSerializers(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Elimina un producto
    """

    def delete(self, request, code):
        producto = self.get_object(code)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@transaction.atomic()
def add_product_detail(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ProductDetailSerializer(data=request.data)
    if serializer.is_valid():
        return create_detail_product(serializer)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@transaction.atomic()
def add_product_detail_purchase(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ProductDetailPurchaseSerializer(data=request.data)
    if serializer.is_valid():
        return create_detail_purchase_product(serializer)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
@transaction.atomic()
def get_products_detail(request, code):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    return get_sub_details_product(code)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_products_detail(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    return get_all_details()


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def search_products(request, search):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    return get_search(search)


@api_view(['GET'])
def get_products_for_user(request):
    return get_products_user()


@api_view(['GET'])
def get_products_detail_for_user(request, code):
    return get_product_detail_user(code)

