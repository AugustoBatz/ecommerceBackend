import jwt
from django.contrib.auth import user_logged_in
from django.http import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from user.models import User
from user.serializers import UserSerializer, CustomSerializer, LoginSerializer, UserSerializerSignUp
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import bcrypt
from user.userresponses import *
from django.db import transaction
# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@transaction.non_atomic_requests
def user_signup(request):
    if (request.method == 'POST'):
        is_mock = request.headers['Mock']
        if (is_mock == 'True'):
            return Response(mock_user(), status=status.HTTP_200_OK)
        serializer = CustomSerializer(data=request.data)
        if serializer.is_valid():
            #obtenemos el arreglo de la funcion encrypt
            encryptArray = encrypt(serializer.data['password'])
            #obtenemos la contrase;a encriptada
            newPassword = encryptArray[0]
            #obtenemos el salt
            saltCreated = encryptArray[1]
            print('antes de crear user')
            user = {
                'first_name': serializer.data['first_name'],
                'last_name': serializer.data['last_name'],
                'phone': serializer.data['phone'],
                'address_a': serializer.data['address_a'],
                'address_b': serializer.data['address_b'],
                'email': serializer.data['email'],
                'is_admin': serializer.data['is_admin'],
                'password': newPassword,
                'username': serializer.data['username'],
                'salt': saltCreated

            }
            print('antes de serializer user')
            serializer_user = UserSerializerSignUp(data=user)
            print('despues de serializer_user')
            print(serializer_user)
            if (serializer_user.is_valid()):

                print('entre a verificar si el serializer de user es valido')
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

def encrypt(txt):
    #pasamos la password a bytes
    passwd = bytes(txt,'utf-8')
    #generamos el salt
    salt = bcrypt.gensalt()
    #hash de la password
    hashed = bcrypt.hashpw(passwd, salt)
    arreglo = [hashed.decode('utf-8'),salt.decode('utf-8')]
    return arreglo

def decrypt(txt,salt, dbpass):
    #pasamos la password a bytes
    #txt seria la pass que se recibe por parte del front
    #salt se obtiene de la base de datos para el usuario
    #dbpass es la pass almacenada en la base de datos para el usuario
    #pasamos la contrase;a encriptada a bytes
    passwd = bytes(txt,'utf-8')
    #pasamos el salt a bytes
    salt = bytes(salt,'utf-8')
    hashed = bcrypt.hashpw(passwd,salt)
    #en hashed tendriamos la pass ingresada por el usuario encriptada
    #pasamos la contrase;a almacenada a bytes
    dbpass = bytes(dbpass,'utf-8')
    #comparamos si ambas contrase;as son iguales
    if hashed == dbpass:
        return True
    else:
        return False


def search_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user


def compare_passwords(txt, user):
    passwd = bytes(txt, 'utf-8')
    salt = bytes(user.salt, 'utf-8') 
    hashed = bcrypt.hashpw(passwd, salt)
    dbpass = bytes(user.password, 'utf-8')
    if hashed == dbpass:
        return True
    else:
        return False


def verify_user(password, username):
    user = search_user(username)
    if user is None:
        return None
    if compare_passwords(password, user):
        return user
    return None


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    data_login = LoginSerializer(data=request.data)
    if data_login.is_valid():
        try:
            username = request.data['username']
            password = request.data['password']
            user = verify_user(password, username)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['username'] = user.username
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)