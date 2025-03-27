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

    # Rutas para los categorias
    path('listadoCategorias/', views.listadoCategorias, name='listadoCategorias'),  # Listar categorías
    path('nuevaCategoria/', views.nuevaCategoria, name='nuevaCategoria'),  # Formulario nueva categoría
    path('guardarCategoria/', views.guardarCategoria, name='guardarCategoria'),  # Guardar nueva categoría
    path('editarCategoria/<int:id>/', views.editarCategoria, name='editarCategoria'),  # Formulario editar categoría
    path('procesarActualizacionCategoria/', views.procesarActualizacionCategoria, name='procesarActualizacionCategoria'),  # Actualizar categoría
    path('eliminarCategoria/<int:id>/', views.eliminarCategoria, name='eliminarCategoria'),  # Eliminar categoría

    # Rutas para los documentos
    path('listadoDocumentos/', views.listadoDocumentos, name='listadoDocumentos'),  # Listar documentos
    path('nuevoDocumento/', views.nuevoDocumento, name='nuevoDocumento'),  # Formulario nuevo documento
    path('guardarDocumento/', views.guardarDocumento, name='guardarDocumento'),  # Guardar nuevo documento
    path('editarDocumento/<int:id>/', views.editarDocumento, name='editarDocumento'),  # Formulario editar documento
    path('procesarActualizacionDocumento/', views.procesarActualizacionDocumento, name='procesarActualizacionDocumento'),  # Actualizar documento
    path('eliminarDocumento/<int:id>/', views.eliminarDocumento, name='eliminarDocumento'),  # Eliminar documento

    # Rutas para las asignaciones de tiempo
    path('listadoAsignaciones/', views.listadoAsignaciones, name='listadoAsignaciones'),  # Listar asignaciones de tiempo
    path('nuevaAsignacion/', views.nuevaAsignacion, name='nuevaAsignacion'),  # Formulario nueva asignación
    path('guardarAsignacion/', views.guardarAsignacion, name='guardarAsignacion'),  # Guardar nueva asignación
    path('editarAsignacion/<int:id>/', views.editarAsignacion, name='editarAsignacion'),  # Formulario editar asignación
    path('procesarActualizacionAsignacion/', views.procesarActualizacionAsignacion, name='procesarActualizacionAsignacion'),  # Actualizar asignación
    path('eliminarAsignacion/<int:id>/', views.eliminarAsignacion, name='eliminarAsignacion'),  # Eliminar asignación
]