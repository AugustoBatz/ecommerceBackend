from django.shortcuts import render
from contactus.serializers import SerializerContact
import jwt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives


# Create your views here.

@api_view(['POST'])
def send_contact_email(request):
    serializer = SerializerContact(data=request.data)
    if serializer.is_valid():
        sendus_email(serializer.data['name'],serializer.data['useremail'],serializer.data['asunt'],serializer.data['message'])
        send_user_email(serializer.data['name'], serializer.data['useremail'])
        return Response(request.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def sendus_email(name, useremail, asunt, message):
    subject, from_email, to = 'Contacto cliente', settings.EMAIL_HOST_USER, 'caqp14@gmail.com'
    text_content = 'This is an important message.'
    html_content = """<html>
        <body style="background-color: #1d3557;">
            <br>
            <br> 
            <h1 style="text-align: center; color: #f1faee;">Solicitud de contacto</h1>
            <div style="max-width: 60%; background-color: #e63946; margin: auto;">
                <h1 style="text-align: center; color: #f1faee; padding-top: 5%;">¡Solicitan contactarnos!</h1>
                <h2 id="user" style="color: #f1faee; text-align: center;">La persona: """ + name +" "+ useremail + """</h2>
                <h2 id="textone" style="color: #f1faee; text-align: center;">Envia el siguiente mensaje: """+ asunt +"""</h2>
                <h2 id="user" style="color: #f1faee; text-align: center;">""" + message + """</h2>
               
            </div>
        </body>
        </html>"""
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_user_email(name, useremail):
    subject, from_email, to = 'Contacto cliente', settings.EMAIL_HOST_USER, useremail
    text_content = 'This is an important message.'
    html_content = """<html>
        <body style="background-color: #1d3557;">
            <br>
            <br> 
            <h1 style="text-align: center; color: #f1faee;">Bienvenido a nuestra tienda</h1>
            <div style="max-width: 60%; background-color: #e63946; margin: auto;">
                <h1 style="text-align: center; color: #f1faee; padding-top: 5%;">¡Hemos recibido tu mensaje!</h1>
                <h2 id="user" style="color: #f1faee; text-align: center;">Estimado: """ + name + """</h2>
                <h2 id="textone" style="color: #f1faee; text-align: center;">Gracias por comunicarte con nosotros</h2>        
            </div>
        </body>
        </html>"""
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()