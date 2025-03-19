from django.contrib import admin
from .models import Usuario, Categoria, Documento, AsignacionTiempo
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Documento)
admin.site.register(AsignacionTiempo)

# Register your models here.
