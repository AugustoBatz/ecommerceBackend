from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all code Books, or create a new Book.
    """
    print('insade user list')
    if request.method == 'GET':
        is_mock = request.headers['Mock']
        if (is_mock == 'True'):
            return Response(list, status=status.HTTP_200_OK)
        print('insade get')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.headers)
        is_mock = request.headers['Mock']
        print('value of mock ' + is_mock)
        if (is_mock == 'True'):
           return Response(request.data, status=status.HTTP_201_CREATED) 
        print('insade post')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

