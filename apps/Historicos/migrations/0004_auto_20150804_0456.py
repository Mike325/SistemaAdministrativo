# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Historicos', '0003_auto_20150804_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='cambioA',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='registro',
            name='cambioDe',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='descripcion',
            field=models.CharField(max_length=150),
        ),
    ]
