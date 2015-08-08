# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0007_auto_20150806_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='fk_suplente',
        ),
        migrations.AddField(
            model_name='suplente',
            name='fk_curso',
            field=models.OneToOneField(default='', to='Departamentos.Curso'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profesor',
            name='codigo_udg',
            field=models.CharField(max_length=9, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(b'^[0-9]*$', b'Use solo caracteres numericos (0-9).')]),
        ),
    ]
