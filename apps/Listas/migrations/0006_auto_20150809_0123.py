# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Listas', '0005_auto_20150809_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='horas_clase',
            field=models.IntegerField(default=0),
        ),
    ]
