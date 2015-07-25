# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0005_remove_usuario_jefedep'),
        ('Departamentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='jefeDep',
            field=models.OneToOneField(null=True, blank=True, to='Usuarios.Usuario'),
        ),
    ]
