# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0003_usuario_jefedep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='jefeDep',
            field=models.ForeignKey(blank=True, to='Departamentos.Departamento', null=True),
        ),
    ]
