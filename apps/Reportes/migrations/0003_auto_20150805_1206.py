# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0006_auto_20150803_2259'),
        ('Reportes', '0002_auto_20150804_0456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporte',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='fk_horario',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='fk_materia',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='fk_profesor',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='fk_seccion',
        ),
        migrations.AddField(
            model_name='reporte',
            name='fk_contrato',
            field=models.ForeignKey(default=False, to='Departamentos.Contrato'),
        ),
    ]
