# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaModificacion', models.DateField(auto_now_add=True)),
                ('horaModificacion', models.TimeField(auto_now_add=True)),
                ('descripcion', models.CharField(max_length=150)),
                ('cambioDe', models.CharField(max_length=30, blank=True)),
                ('cambioA', models.CharField(max_length=30)),
                ('cambioTabla', models.CharField(max_length=30)),
                ('usuario', models.ForeignKey(to='Usuarios.Usuario')),
            ],
        ),
    ]
