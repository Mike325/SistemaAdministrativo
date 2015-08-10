# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Listas', '0003_asistencia_asistio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='horas_clase',
            field=models.TimeField(default=False, blank=True),
        ),
    ]
