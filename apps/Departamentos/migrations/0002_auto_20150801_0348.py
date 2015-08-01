# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='hora_fin',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='hora_ini',
            field=models.TimeField(null=True),
        ),
    ]
