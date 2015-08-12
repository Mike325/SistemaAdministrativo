# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reportes', '0003_auto_20150805_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='comentario',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]
