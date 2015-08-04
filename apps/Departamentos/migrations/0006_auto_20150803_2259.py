# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0005_auto_20150801_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tipo', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'T', b'Tiempo completo'), (b'P', b'Tiempo parcial'), (b'', b'Sin especificar')])),
                ('fk_curso', models.ForeignKey(to='Departamentos.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Suplente',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('periodo_ini', models.DateField(null=True, blank=True)),
                ('periodo_fin', models.DateField(null=True, blank=True)),
                ('fk_profesor', models.ForeignKey(to='Departamentos.Profesor')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_suplente',
            field=models.ForeignKey(blank=True, to='Departamentos.Suplente', null=True),
        ),
    ]
