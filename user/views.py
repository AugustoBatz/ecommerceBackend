from django.http import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer, CustomSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage


# Create your views here.



@api_view(['GET'])
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


@api_view(['POST'])
def user_signup(request):
    if (request.method == 'POST'):
        is_mock = request.headers['Mock']
        if (is_mock == 'True'):
            return Response(mock_user(), status=status.HTTP_200_OK)
        serializer = CustomSerializer(data=request.data)
        if serializer.is_valid():
            user = {
                'name': serializer.data['name'],
                'last_name': serializer.data['last_name'],
                'phone': serializer.data['phone'],
                'address_a': serializer.data['address_a'],
                'address_b': serializer.data['address_b'],
                'email': serializer.data['email'],
                'is_admin': serializer.data['is_admin'],
                'password': serializer.data['password']
            }
            serializer_user = UserSerializer(data=user)
            if (serializer_user.is_valid()):
                user = serializer_user.save()
                data = serializer.data
                del data['password']
                verification_email(data['email'])
                return Response(data, status=status.HTTP_201_CREATED)
                
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def mock_user():
    user = {
        'name': 'User',
        'last_name': 'A',
        'phone': '22446688',
        'address_a': 'Street A',
        'address_b': 'Street B',
        'email': 'mock@email.com',
        'is_admin': False,
    }
    return user;
    
def verification_email(mailuser):
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject = 'Bienvenido a la plataforma', 
        message = 'El proceso de registro esta terminado', 
        from_email = email_from, 
        recipient_list = [mailuser], 
        auth_user = email_from,
        auth_password = settings.EMAIL_HOST_PASSWORD,
        fail_silently = False)



