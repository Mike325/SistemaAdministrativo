# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0008_auto_20150808_0104'),
        ('Historicos', '0004_auto_20150804_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='fk_departamento',
            field=models.ForeignKey(to='Departamentos.Departamento', null=True),
        ),
    ]
