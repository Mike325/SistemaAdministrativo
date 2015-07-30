# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('codigo', models.IntegerField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('profesor', models.CharField(max_length=50)),
                ('categoria', models.CharField(max_length=50)),
                ('horario', models.CharField(max_length=10)),
                ('horasFalta', models.IntegerField()),
                ('codProf', models.ForeignKey(to='Departamentos.Profesor')),
                ('depto', models.ForeignKey(to='Departamentos.Departamento')),
                ('materia', models.ForeignKey(to='Departamentos.Materia')),
                ('secc', models.ForeignKey(to='Departamentos.Seccion')),
            ],
        ),
    ]
