import jwt
from django.contrib.auth import user_logged_in
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from user.models import User
from user.serializers import UserSerializer, CustomSerializer, LoginSerializer, UserSerializerSignUp
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import bcrypt
from django.db import transaction
# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    """
    List all code Books, or create a new Book.
    """
    token = jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6ImF1Z3VzdG9iYXR6QGdtYWlsLmNvbSIsImV4cCI6MTYwMTUyNjE0NCwiZW1haWwiOiJhdWd1c3RvYmF0ekBnbWFpbC5jb20ifQ.H88KRuhnKW1eJNBLnOfWdssVPK6GaxC_iJlxlgbcsrw', settings.SECRET_KEY)
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
@transaction.atomic()
def user_signup(request):
    if (request.method == 'POST'):
        is_mock = request.headers['Mock']
        if (is_mock == 'True'):
            return Response(mock_user(), status=status.HTTP_200_OK)
        serializer = CustomSerializer(data=request.data)
        if serializer.is_valid():
            #obtenemos el arreglo de la funcion encrypt
            print(serializer.data['password'])
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
                name = data['first_name'] + ' ' + data['last_name']
                verification_email(data['email'], name)
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


def verification_email(mailuser, username):
    subject, from_email, to = 'Bienvenido a ******', settings.EMAIL_HOST_USER, mailuser
    text_content = 'This is an important message.'
    html_content = """<html>
        <body style="background-color: #1d3557;">
            <br>
            <br> 
            <h1 style="text-align: center; color: #f1faee;">Bienvenido a nuestra tienda</h1>
            <div style="max-width: 60%; background-color: #e63946; margin: auto;">
                <h1 style="text-align: center; color: #f1faee; padding-top: 5%;">¡Registro exitoso!</h1>
                <h2 id="user" style="color: #f1faee; text-align: center;">Bienvenido: """ + username + """</h2>
                <p style="text-align: center; color: #f1faee; font-size: x-large;">Te agradecemos mucho el formar parte de nuestra familia de usuarios, esperamos te sorprendan nuestra grandes ofertas</p>
                <img src="https://images.pexels.com/photos/34577/pexels-photo.jpg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940" style="margin: auto; display: block; max-width: 80%; padding-bottom: 5%;" >
            </div>
        </body>
        </html>"""
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


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