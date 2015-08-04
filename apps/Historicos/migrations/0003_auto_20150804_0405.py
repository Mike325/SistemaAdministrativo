# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Historicos', '0002_auto_20150804_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='descripcion',
            field=models.CharField(max_length=300),
        ),
    ]
