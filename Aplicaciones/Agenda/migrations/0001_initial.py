# Generated by Django 4.0.6 on 2025-03-19 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_cat', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cat', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usu', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_usu', models.CharField(max_length=100)),
                ('apellido_usu', models.CharField(max_length=100)),
                ('correo_usu', models.EmailField(max_length=100, unique=True)),
                ('usuario_usu', models.CharField(max_length=100, unique=True)),
                ('contrasena_usu', models.CharField(max_length=255)),
                ('rol_usu', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id_doc', models.AutoField(primary_key=True, serialize=False)),
                ('titulo_doc', models.CharField(max_length=255)),
                ('descripcion_doc', models.TextField(blank=True, null=True)),
                ('tipo_doc', models.CharField(choices=[('informe', 'Informe'), ('acta', 'Acta'), ('resolucion', 'Resolución')], max_length=50)),
                ('fecha_subida_doc', models.DateTimeField(auto_now_add=True)),
                ('fecha_asignacion_doc', models.DateField(blank=True, null=True)),
                ('fecha_limite_doc', models.DateField(blank=True, null=True)),
                ('fecha_entrega_doc', models.DateField(blank=True, null=True)),
                ('estado_doc', models.CharField(blank=True, choices=[('en tiempo', 'En Tiempo'), ('retrasado', 'Retrasado'), ('incumplido', 'Incumplido')], default='en tiempo', max_length=15, null=True)),
                ('id_cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Agenda.categoria')),
                ('id_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agenda.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionTiempo',
            fields=[
                ('id_asi', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asignacion_asi', models.DateTimeField(auto_now_add=True)),
                ('fecha_limite_asi', models.DateField()),
                ('id_doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agenda.documento')),
                ('id_usu_asignado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignado', to='Agenda.usuario')),
                ('id_usu_asignador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignador', to='Agenda.usuario')),
            ],
        ),
    ]
