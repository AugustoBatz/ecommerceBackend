from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductoSerializers, ProductoModificacionSerializers


class productoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    """
    Ingresa un producto
    """
    def post(self,request):
        serializer = ProductoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)
    
    """
    Obtiene un producto
    """
    def get(self, request):
        codigo = request.GET.get('code')
        if codigo is None:
            try:
                productos = Product.objects.all()
            except Product.DoesNotExist:
                return Response()
            serializer = ProductoSerializers(productos, many=True)
            return Response(serializer.data)
        else:
            try:
                productos = Product.objects.get(code=codigo)
            except Product.DoesNotExist:
                return Response({'Error': 'El código ingresado no existe'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductoSerializers(productos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Modifica un producto
    """
    def put(self, request):
        codigo = request.GET.get('code')
        try:
            producto = Product.objects.get(code=codigo)
            serializer = ProductoModificacionSerializers(producto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'Error': 'El código ingresado no existe'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """
    Elimina un producto
    """

    def delete(self, request):
        codigo = request.GET.get('code')

        if codigo is None:
            try:
                producto = Product.objects.get(code=codigo)
                producto.delete()
                return Response({'mensaje':'Producto eliminado con éxito'}, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({'Error':'No existe el producto'}, status=status.HTTP_404_NOT_FOUND)

