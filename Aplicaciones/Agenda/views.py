from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Usuario

def home(request):
    return render(request, 'home.html')

def reset(request):
    email_sent = False
    
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
            email_sent = True

        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese correo electrónico.')

    return render(request, 'reset.html', {'email_sent': email_sent})

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
    nombre = request.POST["nombre_usu"]
    apellido = request.POST["apellido_usu"]
    correo = request.POST["correo_usu"]
    usuario = request.POST["usuario_usu"]
    contrasena = request.POST["contrasena_usu"]
    rol = request.POST["rol_usu"]
    imagen = request.FILES.get("foto")

    if not correo or '@' not in correo:
        messages.error(request, "El correo electrónico no es válido.")
        return redirect('nuevoUsuario')
    if len(contrasena) < 6:
        messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
        return redirect('nuevoUsuario')

    if Usuario.objects.filter(usuario_usu=usuario).exists():
        messages.error(request, "El nombre de usuario ya está registrado.")
        return redirect('nuevoUsuario')

    Usuario.objects.create(
        nombre_usu=nombre,
        apellido_usu=apellido,
        correo_usu=correo,
        usuario_usu=usuario,
        contrasena_usu=contrasena,
        rol_usu=rol,
        foto=imagen
    )
    messages.success(request, "Usuario registrado exitosamente.")
    return redirect('listadoUsuarios')

def procesarActualizacionUsuario(request):
    id = request.POST['id_usu']
    nombre = request.POST['nombre_usu']
    apellido = request.POST['apellido_usu']
    correo = request.POST['correo_usu']
    usuario = request.POST['usuario_usu']
    contrasena = request.POST.get('contrasena_usu', None)
    rol = request.POST['rol_usu']
    imagen = request.FILES.get('foto')

    usuarioConsultado = get_object_or_404(Usuario, id_usu=id)

    if not correo or '@' not in correo:
        messages.error(request, "El correo electrónico no es válido.")
        return redirect('editarUsuario', id=id)
    if contrasena and len(contrasena) < 6:
        messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
        return redirect('editarUsuario', id=id)

    cambios = False
    if usuarioConsultado.nombre_usu != nombre:
        usuarioConsultado.nombre_usu = nombre
        cambios = True
    if usuarioConsultado.apellido_usu != apellido:
        usuarioConsultado.apellido_usu = apellido
        cambios = True
    if usuarioConsultado.correo_usu != correo:
        usuarioConsultado.correo_usu = correo
        cambios = True
    if usuarioConsultado.usuario_usu != usuario:
        usuarioConsultado.usuario_usu = usuario
        cambios = True
    if contrasena:
        usuarioConsultado.contrasena_usu = contrasena
        cambios = True
    if usuarioConsultado.rol_usu != rol:
        usuarioConsultado.rol_usu = rol
        cambios = True
    if imagen:
        usuarioConsultado.foto = imagen
        cambios = True

    if cambios:
        usuarioConsultado.save()
        messages.success(request, "Usuario actualizado exitosamente.")
    else:
        messages.info(request, "No se realizaron cambios.")

    return redirect('listadoUsuarios')