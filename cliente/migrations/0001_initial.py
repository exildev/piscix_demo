# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 02:57
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0002_auto_20160319_0257'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.TextField(max_length=400)),
                ('telefono', models.IntegerField()),
                ('fecha', models.DateField(verbose_name='Fecha de nacimiento')),
                ('piscina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Activo')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='repotes')),
            ],
            options={
                'verbose_name': 'Imagen de reporte',
                'verbose_name_plural': 'Imagenes de reporte',
            },
        ),
        migrations.CreateModel(
            name='Piscinero',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('identificacion', models.CharField(max_length=100)),
                ('direccion', models.TextField(max_length=400)),
                ('telefono', models.IntegerField()),
                ('fecha', models.DateField(verbose_name='Fecha de nacimiento')),
                ('padre', models.CharField(max_length=200)),
                ('madre', models.CharField(max_length=200)),
                ('estado_civil', models.CharField(choices=[('Soltero', 'Soltero'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado')], max_length=100)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=400)),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente')),
                ('reporta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Piscinero')),
            ],
        ),
        migrations.CreateModel(
            name='TipoReporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='reporte',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.TipoReporte', verbose_name='Tipo de novedad'),
        ),
        migrations.AddField(
            model_name='imagenr',
            name='reporte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Reporte'),
        ),
    ]
