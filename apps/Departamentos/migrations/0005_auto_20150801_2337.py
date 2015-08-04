# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0004_auto_20150801_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='fk_aulas',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='fk_edifs',
        ),
        migrations.AddField(
            model_name='horario',
            name='fk_aula',
            field=models.ForeignKey(blank=True, to='Departamentos.Aula', null=True),
        ),
        migrations.AddField(
            model_name='horario',
            name='fk_edif',
            field=models.ForeignKey(blank=True, to='Departamentos.Edificio', null=True),
        ),
    ]
