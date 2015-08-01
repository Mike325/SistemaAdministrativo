# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0002_auto_20150801_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='hora_fin',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='hora_ini',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
