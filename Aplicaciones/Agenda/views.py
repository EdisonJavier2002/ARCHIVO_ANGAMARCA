from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Usuario

def home(request):
    return render(request, 'home.html')

def reset(request):
    if request.method == 'POST':
        correo_usu = request.POST.get('correo_usu')
        try:
            user = Usuario.objects.get(correo_usu=correo_usu)
            new_password = get_random_string(8)
            user.contrasena_usu = new_password
            user.save()
            send_mail(
                'Recuperación de contraseña',
                f'Su nueva contraseña es: {new_password}',
                'noreply@tu-dominio.com',
                [correo_usu],
                fail_silently=False,
            )
            messages.success(request, 'Se ha enviado una nueva contraseña a su correo electrónico.')
            return redirect('login')
        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese correo electrónico.')
    return render(request, 'reset.html')


def login(request):
    if request.method == 'POST':
        usuario_usu = request.POST.get('usuario_usu')
        contrasena_usu = request.POST.get('contrasena_usu')

        try:
            user = Usuario.objects.get(usuario_usu=usuario_usu)
            if contrasena_usu == user.contrasena_usu:
                request.session['user_id'] = user.id_usu
                return redirect('home')  # Redirige a la vista 'home'
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')