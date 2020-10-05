from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductoSerializers
from django.http import Http404
from rest_framework import status
from user.views import *


class productoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    """
    Ingresa un producto
    """
    def post(self,request):
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
        serializer = ProductoSerializers(productos, many = True)
        return Response(serializer.data)



class productoEspecificoAPIView(APIView):

    """
    Obtiene la lista de productos
    """
    def get_object(self, code):
        try:
            return Product.objects.get(code = code)
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
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    """
    Elimina un producto
    """
    def delete(self, request, code):
        producto = self.get_object(code)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
