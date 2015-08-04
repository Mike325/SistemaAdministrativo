# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0003_auto_20150801_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='fk_aula',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='fk_edif',
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_aulas',
            field=models.ManyToManyField(to='Departamentos.Aula', blank=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_edifs',
            field=models.ManyToManyField(to='Departamentos.Edificio', blank=True),
        ),
    ]
