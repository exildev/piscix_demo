# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 17:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20160319_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulo',
            name='tiempo_entrega',
        ),
    ]
