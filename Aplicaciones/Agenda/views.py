from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os  # Añadir esta línea
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.utils.crypto import get_random_string
from .models import Usuario
from sendgrid import SendGridAPIClient
from .utils import get_email_settings
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from decouple import config

def home(request):
    return render(request, 'home.html')

def send_reset_email(user_email):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user_email,
        subject='Restablecer tu contraseña',
        html_content='<p>Haz clic en este <a href="#">enlace</a> para restablecer tu contraseña.</p>'
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(f'Error al enviar correo: {e}')

def reset(request):
    email_sent = False
    
    if request.method == 'POST':
        correo_usu = request.POST.get('correo_usu')
        try:
            # Verificar si el correo está registrado
            user = Usuario.objects.get(correo_usu=correo_usu)
            new_password = get_random_string(8)
            user.contrasena_usu = new_password
            user.save()

            # Envío del correo
            subject = 'Recuperación de contraseña'
            message = f'Su nueva contraseña es: {new_password}'
            from_email = config('DEFAULT_FROM_EMAIL')
            to_emails = correo_usu

            mail = Mail(
                from_email=from_email,
                to_emails=to_emails,
                subject=subject,
                plain_text_content=message
            )

            try:
                sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sg.send(mail)
                if response.status_code == 202:
                    messages.success(request, 'Se ha enviado una nueva contraseña a su correo electrónico.')
                    email_sent = True
                else:
                    messages.error(request, 'No se pudo enviar el correo electrónico.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al enviar el correo: {e}')

        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese correo electrónico.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')

    return render(request, 'reset.html', {'email_sent': email_sent})

def get_email_settings(email_user):
    """
    Función que devuelve la configuración SMTP basada en el dominio del usuario de correo.
    Debe retornar configuraciones de correo según el dominio.
    """
    if '@gmail.com' in email_user:
        return {
            "EMAIL_HOST": "smtp.gmail.com",
            "EMAIL_PORT": 587,
            "EMAIL_USE_TLS": True,
            "EMAIL_HOST_USER": email_user,
            "EMAIL_HOST_PASSWORD": os.getenv("GMAIL_PASSWORD"),  # Usar variable de entorno
        }
    elif '@yahoo.com' in email_user:
        return {
            "EMAIL_HOST": "smtp.mail.yahoo.com",
            "EMAIL_PORT": 587,
            "EMAIL_USE_TLS": True,
            "EMAIL_HOST_USER": email_user,
            "EMAIL_HOST_PASSWORD": os.getenv("YAHOO_PASSWORD"),  # Usar variable de entorno
        }
    elif '@outlook.com' in email_user or '@hotmail.com' in email_user:
        return {
            "EMAIL_HOST": "smtp.office365.com",
            "EMAIL_PORT": 587,
            "EMAIL_USE_TLS": True,
            "EMAIL_HOST_USER": email_user,
            "EMAIL_HOST_PASSWORD": os.getenv("OUTLOOK_PASSWORD"),  # Usar variable de entorno
        }
    else:
        return {
            "EMAIL_HOST": "smtp.dominio.com",
            "EMAIL_PORT": 587,
            "EMAIL_USE_TLS": True,
            "EMAIL_HOST_USER": "usuario@dominio.com",
            "EMAIL_HOST_PASSWORD": os.getenv("CUSTOM_EMAIL_PASSWORD"),  # Usar variable de entorno
        }

def login(request):
    if request.method == 'POST':
        usuario_usu = request.POST.get('usuario_usu')
        contrasena_usu = request.POST.get('contrasena_usu')

        try:
            user = Usuario.objects.only('usuario_usu', 'contrasena_usu').get(usuario_usu=usuario_usu)
            if contrasena_usu == user.contrasena_usu:
                request.session['user_id'] = user.id_usu
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')


#----------------------------------------USUARIOS-------------------------

def listadoUsuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "listadoUsuarios.html", {'usuarios': usuarios})

def eliminarUsuario(request, id):
    usuarioEliminar = get_object_or_404(Usuario, id_usu=id)
    usuarioEliminar.delete()
    messages.success(request, "Usuario eliminado exitosamente.")
    return redirect('listadoUsuarios')

def nuevoUsuario(request):
    return render(request, 'nuevoUsuario.html')

def editarUsuario(request, id):
    usuarioEditar = get_object_or_404(Usuario, id_usu=id)
    return render(request, 'editarUsuario.html', {'usuarioEditar': usuarioEditar})

def guardarUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usu', '').strip()
        apellido = request.POST.get('apellido_usu', '').strip()
        correo = request.POST.get('correo_usu', '').strip()
        usuario = request.POST.get('usuario_usu', '').strip()
        contrasena = request.POST.get('contrasena_usu', '').strip()
        rol = request.POST.get('rol_usu', '').strip()
        foto = request.FILES.get('foto')

        # Validar que todos los campos estén llenos
        if not all([nombre, apellido, correo, usuario, contrasena, rol, foto]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('nuevoUsuario')

        # Guardar el usuario en la base de datos
        nuevo_usuario = Usuario(
            nombre_usu=nombre,
            apellido_usu=apellido,
            correo_usu=correo,
            usuario_usu=usuario,
            contrasena_usu=contrasena,
            rol_usu=rol,
            foto=foto
        )
        nuevo_usuario.save()

        messages.success(request, 'Usuario guardado exitosamente.')
        return redirect('listadoUsuarios')
    else:
        return redirect('nuevoUsuario')

def procesarActualizacionUsuario(request):
    if request.method == 'POST':
        id_usu = request.POST.get('id_usu')
        usuario = get_object_or_404(Usuario, id_usu=id_usu)

        nombre = request.POST.get('nombre_usu', '').strip()
        apellido = request.POST.get('apellido_usu', '').strip()
        correo = request.POST.get('correo_usu', '').strip()
        usuario_usu = request.POST.get('usuario_usu', '').strip()
        contrasena = request.POST.get('contrasena_usu', '').strip()
        rol = request.POST.get('rol_usu', '').strip()
        foto = request.FILES.get('foto')

        if not nombre.isalpha():
            messages.error(request, "El nombre solo debe contener letras.")
            return redirect('editarUsuario', id_usu=id_usu)

        if not apellido.isalpha():
            messages.error(request, "El apellido solo debe contener letras.")
            return redirect('editarUsuario', id_usu=id_usu)

        if '@' not in correo:
            messages.error(request, "El correo no es válido.")
            return redirect('editarUsuario', id_usu=id_usu)

        if contrasena and len(contrasena) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
            return redirect('editarUsuario', id_usu=id_usu)

        usuario.nombre_usu = nombre
        usuario.apellido_usu = apellido
        usuario.correo_usu = correo
        usuario.usuario_usu = usuario_usu
        usuario.rol_usu = rol

        if contrasena:
            usuario.contrasena_usu = contrasena

        if foto:
            usuario.foto = foto

        usuario.save()
        messages.success(request, "Usuario actualizado exitosamente.")
        return redirect('listadoUsuarios')