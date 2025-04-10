from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os  # Añadir esta línea
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.utils.crypto import get_random_string
from .models import Usuario, Categoria, Documento, AsignacionTiempo
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

def login(request):
    if request.method == 'POST':
        usuario_usu = request.POST.get('usuario_usu')
        contrasena_usu = request.POST.get('contrasena_usu')

        try:
            user = Usuario.objects.only('usuario_usu', 'contrasena_usu').get(usuario_usu=usuario_usu)
            if contrasena_usu == user.contrasena_usu:
                request.session['user_id'] = user.id_usu
                messages.success(request, f'Bienvenido, {user.usuario_usu}!')  # Mensaje de bienvenida
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
    
#----------------------------------------CATEGORIAS-------------------------
def listadoCategorias(request):
    categorias = Categoria.objects.all()
    return render(request, "listadoCategorias.html", {'categorias': categorias})

def nuevaCategoria(request):
    return render(request, 'nuevaCategoria.html')

def guardarCategoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_cat', '').strip()

        if not nombre:
            messages.error(request, 'El nombre de la categoría es obligatorio.')
            return redirect('nuevaCategoria')

        if Categoria.objects.filter(nombre_cat=nombre).exists():
            messages.error(request, 'Esta categoría ya existe.')
            return redirect('nuevaCategoria')

        nueva_categoria = Categoria(nombre_cat=nombre)
        nueva_categoria.save()

        messages.success(request, 'Categoría guardada exitosamente.')
        return redirect('listadoCategorias')

    return redirect('nuevaCategoria')

def editarCategoria(request, id):
    categoriaEditar = get_object_or_404(Categoria, id_cat=id)
    return render(request, 'editarCategoria.html', {'categoriaEditar': categoriaEditar})

def procesarActualizacionCategoria(request):
    if request.method == 'POST':
        id_cat = request.POST.get('id_cat')
        categoria = get_object_or_404(Categoria, id_cat=id_cat)

        nombre = request.POST.get('nombre_cat', '').strip()

        if not nombre:
            messages.error(request, "El nombre de la categoría es obligatorio.")
            return redirect('editarCategoria', id=id_cat)

        if Categoria.objects.filter(nombre_cat=nombre).exclude(id_cat=id_cat).exists():
            messages.error(request, "Esta categoría ya existe.")
            return redirect('editarCategoria', id=id_cat)

        categoria.nombre_cat = nombre
        categoria.save()

        messages.success(request, "Categoría actualizada exitosamente.")
        return redirect('listadoCategorias')

    return redirect('listadoCategorias')

def eliminarCategoria(request, id):
    categoriaEliminar = get_object_or_404(Categoria, id_cat=id)
    categoriaEliminar.delete()
    messages.success(request, "Categoría eliminada exitosamente.")
    return redirect('listadoCategorias')

#----------------------------------------DOCUMENTOS-------------------------
def listadoDocumentos(request):
    documentos = Documento.objects.all()
    return render(request, "listadoDocumentos.html", {'documentos': documentos})

# Eliminar documento
def eliminarDocumento(request, id):
    documentoEliminar = get_object_or_404(Documento, id_doc=id)
    if documentoEliminar.archivo_doc:  # Eliminar el archivo físico si existe
        documentoEliminar.archivo_doc.delete()
    documentoEliminar.delete()
    messages.success(request, "Documento eliminado exitosamente.")
    return redirect('listadoDocumentos')

# Formulario para nuevo documento
def nuevoDocumento(request):
    categorias = Categoria.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'nuevoDocumento.html', {'categorias': categorias, 'usuarios': usuarios})

# Formulario para editar documento
def editarDocumento(request, id):
    documentoEditar = get_object_or_404(Documento, id_doc=id)
    categorias = Categoria.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'editarDocumento.html', {'documentoEditar': documentoEditar, 'categorias': categorias, 'usuarios': usuarios})

# Guardar nuevo documento
def guardarDocumento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo_doc', '').strip()
        descripcion = request.POST.get('descripcion_doc', '').strip()
        tipo = request.POST.get('tipo_doc', '').strip()
        id_cat = request.POST.get('id_cat', None)
        id_usu = request.POST.get('id_usu', None)
        estado = request.POST.get('estado_doc', 'en tiempo')
        archivo = request.FILES.get('archivo_doc', None)  # Obtener el archivo subido

        # Validaciones
        if not titulo or not tipo or not id_usu:
            messages.error(request, 'Título, tipo de documento y usuario son obligatorios.')
            return redirect('nuevoDocumento')

        # Guardar el documento
        nuevo_documento = Documento(
            titulo_doc=titulo,
            descripcion_doc=descripcion,
            tipo_doc=tipo,
            id_cat=Categoria.objects.get(id_cat=id_cat) if id_cat else None,
            id_usu=Usuario.objects.get(id_usu=id_usu),
            estado_doc=estado,
            archivo_doc=archivo  # Guardar el archivo
        )
        nuevo_documento.save()

        messages.success(request, 'Documento guardado exitosamente.')
        return redirect('listadoDocumentos')
    else:
        return redirect('nuevoDocumento')

# Actualizar documento
def procesarActualizacionDocumento(request):
    if request.method == 'POST':
        id_doc = request.POST.get('id_doc')
        documento = get_object_or_404(Documento, id_doc=id_doc)

        titulo = request.POST.get('titulo_doc', '').strip()
        descripcion = request.POST.get('descripcion_doc', '').strip()
        tipo = request.POST.get('tipo_doc', '').strip()
        id_cat = request.POST.get('id_cat', None)
        id_usu = request.POST.get('id_usu', None)
        estado = request.POST.get('estado_doc', 'en tiempo')
        archivo = request.FILES.get('archivo_doc', None)  # Obtener el archivo subido

        if not titulo or not tipo or not id_usu:
            messages.error(request, "Título, tipo de documento y usuario son obligatorios.")
            return redirect('editarDocumento', id=id_doc)

        # Actualizar los valores
        documento.titulo_doc = titulo
        documento.descripcion_doc = descripcion
        documento.tipo_doc = tipo
        documento.id_cat = Categoria.objects.get(id_cat=id_cat) if id_cat else None
        documento.id_usu = Usuario.objects.get(id_usu=id_usu)
        documento.estado_doc = estado

        # Si se sube un nuevo archivo, eliminar el anterior y guardar el nuevo
        if archivo:
            if documento.archivo_doc:  # Eliminar el archivo existente si hay uno
                documento.archivo_doc.delete()
            documento.archivo_doc = archivo

        documento.save()
        messages.success(request, "Documento actualizado exitosamente.")
        return redirect('listadoDocumentos')
    

#----------------------------------------ASIGNACION TIEMPO-------------------------

# Listado de asignaciones de tiempo
def listadoAsignaciones(request):
    asignaciones = AsignacionTiempo.objects.all()
    return render(request, "listadoAsignaciones.html", {'asignaciones': asignaciones})

# Eliminar asignación de tiempo
def eliminarAsignacion(request, id):
    asignacionEliminar = get_object_or_404(AsignacionTiempo, id_asi=id)
    asignacionEliminar.delete()
    messages.success(request, "Asignación eliminada exitosamente.")
    return redirect('listadoAsignaciones')

# Formulario para nueva asignación de tiempo
def nuevaAsignacion(request):
    documentos = Documento.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'nuevaAsignacion.html', {'documentos': documentos, 'usuarios': usuarios})

# Formulario para editar asignación de tiempo
def editarAsignacion(request, id):
    asignacionEditar = get_object_or_404(AsignacionTiempo, id_asi=id)
    documentos = Documento.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'editarAsignacion.html', {'asignacionEditar': asignacionEditar, 'documentos': documentos, 'usuarios': usuarios})

# Guardar nueva asignación de tiempo
def guardarAsignacion(request):
    if request.method == 'POST':
        id_doc = request.POST.get('id_doc', None)
        id_usu_asignador = request.POST.get('id_usu_asignador', None)
        id_usu_asignado = request.POST.get('id_usu_asignado', None)
        fecha_limite = request.POST.get('fecha_limite_asi', None)

        # Validaciones
        if not id_doc or not id_usu_asignador or not id_usu_asignado or not fecha_limite:
            messages.error(request, 'Documento, usuario asignador, usuario asignado y fecha límite son obligatorios.')
            return redirect('nuevaAsignacion')

        # Guardar la asignación de tiempo
        nueva_asignacion = AsignacionTiempo(
            id_doc=Documento.objects.get(id_doc=id_doc),
            id_usu_asignador=Usuario.objects.get(id_usu=id_usu_asignador),
            id_usu_asignado=Usuario.objects.get(id_usu=id_usu_asignado),
            fecha_limite_asi=fecha_limite
        )
        nueva_asignacion.save()

        messages.success(request, 'Asignación guardada exitosamente.')
        return redirect('listadoAsignaciones')
    else:
        return redirect('nuevaAsignacion')

# Actualizar asignación de tiempo
def procesarActualizacionAsignacion(request):
    if request.method == 'POST':
        id_asi = request.POST.get('id_asi')
        asignacion = get_object_or_404(AsignacionTiempo, id_asi=id_asi)

        id_doc = request.POST.get('id_doc', None)
        id_usu_asignador = request.POST.get('id_usu_asignador', None)
        id_usu_asignado = request.POST.get('id_usu_asignado', None)
        fecha_limite = request.POST.get('fecha_limite_asi', None)

        if not id_doc or not id_usu_asignador or not id_usu_asignado or not fecha_limite:
            messages.error(request, 'Documento, usuario asignador, usuario asignado y fecha límite son obligatorios.')
            return redirect('editarAsignacion', id=id_asi)

        # Actualizar los valores
        asignacion.id_doc = Documento.objects.get(id_doc=id_doc)
        asignacion.id_usu_asignador = Usuario.objects.get(id_usu=id_usu_asignador)
        asignacion.id_usu_asignado = Usuario.objects.get(id_usu=id_usu_asignado)
        asignacion.fecha_limite_asi = fecha_limite

        asignacion.save()
        messages.success(request, "Asignación actualizada exitosamente.")
        return redirect('listadoAsignaciones')

