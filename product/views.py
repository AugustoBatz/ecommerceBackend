from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductoSerializers, ProductoModificacionSerializers

# Create your views here.
class productoAPIView(APIView):

    """
    Ingresa un producto
    """
    def post(self,request):

        serializer = ProductoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
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
            serializer = ProductoSerializers(productos, many = True)
            return Response(serializer.data)
        else:
            try:
                productos = Product.objects.get(code = codigo)
            except Product.DoesNotExist:
                return Response({'Error': 'El código ingresado no existe'})

            serializer = ProductoSerializers(productos, many=True)
            return Response(serializer.data)

    """
    Modifica un producto
    """
    def put(self, request):
        codigo = request.GET.get('code')
        try:
            producto = Product.objects.get(code = codigo)
            serializer = ProductoModificacionSerializer(producto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'Error': 'El código ingresado no existe'})
        
        return Response(serializer.errors)
    
    """
    Elimina un producto
    """

    def delete(self, request):
        codigo = request.GET.get('code')

        if codigo is None:
            try:
                producto = Product.objects.get(code=codigo)
                producto.delete()
                return Response({'mensaje':'Producto eliminado con éxito'})
            except Product.DoesNotExist:
                return Response({'Error':'No existe el producto'}) 

