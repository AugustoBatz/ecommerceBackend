from django.http import JsonResponse

def not_found():
    data = {
        'code': 404,
        'description': 'El usuario ingresado no se encuentra registrado en la pagina. Verifique que los datos esten ingresados correctamente e intente de nuevo'
    }
    return data
    #return JsonResponse(data)

def incorrect_password():
    data = {
        'code': 401,
        'description': 'Contraseña incorrecta, vuelva a intentarlo'

    }
    return data
    #return JsonResponse(data)

def correct_user():
    data = {
        'code': 200,
        'description': 'Haz sido reconocido'
    }
    return data
    #return JsonResponse(data)

def password_change():
    data = {
        'code': 100,
        'description': 'La contraseña ha sido reeestablecida correctamente'
    }
    return data
    