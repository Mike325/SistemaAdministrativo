# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0006_auto_20150803_2259'),
        ('Reportes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporte',
            name='codProf',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='depto',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='horario',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='materia',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='profesor',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='secc',
        ),
        migrations.AddField(
            model_name='reporte',
            name='fk_depto',
            field=models.ForeignKey(default=False, to='Departamentos.Departamento'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='fk_horario',
            field=models.ManyToManyField(to='Departamentos.Horario', blank=True),
        ),
        migrations.AddField(
            model_name='reporte',
            name='fk_materia',
            field=models.ForeignKey(default=False, to='Departamentos.Materia'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='fk_profesor',
            field=models.ForeignKey(default=False, to='Departamentos.Profesor'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='fk_seccion',
            field=models.ForeignKey(default=False, to='Departamentos.Seccion'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='id',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reporte',
            name='categoria',
            field=models.CharField(default=False, max_length=30, blank=True),
        ),
    ]
