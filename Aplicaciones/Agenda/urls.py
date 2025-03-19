from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),  # Ruta para la página principal
    path('reset/', views.reset, name='reset'),

    # Rutas para los usuarios
    path('listadoUsuarios/', views.listadoUsuarios, name='listadoUsuarios'),  # Listar usuarios
    path('nuevoUsuario/', views.nuevoUsuario, name='nuevoUsuario'),  # Formulario nuevo usuario
    path('guardarUsuario/', views.guardarUsuario, name='guardarUsuario'),  # Guardar nuevo usuario
    path('editarUsuario/<int:id>/', views.editarUsuario, name='editarUsuario'),  # Formulario editar usuario
    path('procesarActualizacionUsuario/', views.procesarActualizacionUsuario, name='procesarActualizacionUsuario'),  # Actualizar usuario
    path('eliminarUsuario/<int:id>/', views.eliminarUsuario, name='eliminarUsuario'),  # Eliminar usuario
]