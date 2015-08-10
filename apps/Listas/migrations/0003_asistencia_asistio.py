# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Listas', '0002_auto_20150808_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='asistio',
            field=models.BooleanField(default=False),
        ),
    ]
