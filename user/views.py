from django.http import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer, CustomSerializer, LoginSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import bcrypt
from user.userresponses import *
from django.db import transaction
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
                'name': serializer.data['name'],
                'last_name': serializer.data['last_name'],
                'phone': serializer.data['phone'],
                'address_a': serializer.data['address_a'],
                'address_b': serializer.data['address_b'],
                'email': serializer.data['email'],
                'is_admin': serializer.data['is_admin'],
                'password': newPassword,
                'salt': saltCreated

            }
            print('antes de serializer user')
            serializer_user = UserSerializer(data=user)
#            serializer_user = UserSerializer(data = {'name': serializer.data['name'], 'last_name': serializer.data['last_name'], 'phone': serializer.data['phone'], 'address_a': serializer.data['address_a'], 'address_b': serializer.data['address_b'], 'email': serializer.data['email'], 'is_admin': serializer.data['is_admin'], 'password': newPassword, 'salt': saltCreated})
#            serializer_user.save(owner = saltCreated)
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

def search_user(email):
    try:
        user = User.objects.get(email=email)
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

def verificar_usuario(password,mail):
    user = search_user(mail)
    if user == None:
        return Response(not_found(), status=status.HTTP_404_NOT_FOUND)
    if(compare_passwords(password, user) == True):
    #    print('si son iguales')
        return Response(correct_user(), status=status.HTTP_200_OK)
    #print('no autorizado')    
    return Response(incorrect_password(), status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def login(request):
    if (request.method == 'POST'):
        is_mock = request.headers['mock']
        if (is_mock == 'True'):
            return False
        datosLogin = LoginSerializer(data=request.data)
        if datosLogin.is_valid():
            datos = {
                'password': datosLogin.data['password'],
                'email': datosLogin.data['email']
            }
            return verificar_usuario(datos['password'], datos['email'])

