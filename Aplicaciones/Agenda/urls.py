from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),  # Ruta para la página principal
    path('reset/', views.reset, name='reset'),
    # otras rutas...
]