# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0008_auto_20150808_0104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('horas_clase', models.IntegerField(default=False)),
                ('fk_contrato', models.ForeignKey(to='Departamentos.Contrato')),
            ],
        ),
    ]
