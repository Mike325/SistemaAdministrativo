# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0001_initial'),
        ('Usuarios', '0002_auto_20150723_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='jefeDep',
            field=models.ForeignKey(default=1, blank=True, to='Departamentos.Departamento'),
            preserve_default=False,
        ),
    ]
