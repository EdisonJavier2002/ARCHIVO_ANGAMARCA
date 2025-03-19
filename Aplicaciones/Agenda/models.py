from django.db import models

# MODELO USUARIO
class Usuario(models.Model):
    id_usu = models.AutoField(primary_key=True)
    nombre_usu = models.CharField(max_length=100)
    apellido_usu = models.CharField(max_length=100)
    correo_usu = models.EmailField(max_length=100, unique=True)
    usuario_usu = models.CharField(max_length=100, unique=True)
    contrasena_usu = models.CharField(max_length=255)
    rol_usu = models.CharField(max_length=50)
    imagen_usu = models.ImageField(upload_to='usuarios/', blank=True, null=True)  # Nuevo campo de imagen
    
    def __str__(self):
        return f"{self.id_usu}: {self.nombre_usu} {self.apellido_usu} ({self.rol_usu})"

# MODELO CATEGORIA
class Categoria(models.Model):
    id_cat = models.AutoField(primary_key=True)
    nombre_cat = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre_cat

# MODELO DOCUMENTO
class Documento(models.Model):
    id_doc = models.AutoField(primary_key=True)
    titulo_doc = models.CharField(max_length=255)
    descripcion_doc = models.TextField(blank=True, null=True)
    tipo_doc = models.CharField(
        max_length=50,
        choices=[('informe', 'Informe'), ('acta', 'Acta'), ('resolucion', 'Resolución')],
    )
    id_cat = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    fecha_subida_doc = models.DateTimeField(auto_now_add=True) #solo para informes
    fecha_asignacion_doc = models.DateField(null=True, blank=True) #solo para informes
    fecha_limite_doc = models.DateField(null=True, blank=True) #solo para informes
    fecha_entrega_doc = models.DateField(blank=True, null=True) #solo para informes
    id_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado_doc = models.CharField(
        max_length=15,
        choices=[('en tiempo', 'En Tiempo'), ('retrasado', 'Retrasado'), ('incumplido', 'Incumplido')],
        default='en tiempo',
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.titulo_doc} - {self.estado_doc}"

# MODELO ASIGNACION TIEMPO
class AsignacionTiempo(models.Model):
    id_asi = models.AutoField(primary_key=True)
    id_doc = models.ForeignKey(Documento, on_delete=models.CASCADE)
    id_usu_asignador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asignador')
    id_usu_asignado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asignado')
    fecha_asignacion_asi = models.DateTimeField(auto_now_add=True)
    fecha_limite_asi = models.DateField()
    
    def __str__(self):
        return f"{self.id_usu_asignado} debe subir {self.id_doc} antes del {self.fecha_limite_asi}"
