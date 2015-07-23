# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.CharField(max_length=6, serialize=False, primary_key=True)),
                ('fecha_ini', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('NRC', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('fk_area', models.ForeignKey(to='Departamentos.Area')),
                ('fk_aula', models.ForeignKey(to='Departamentos.Aula')),
                ('fk_ciclo', models.ForeignKey(to='Departamentos.Ciclo')),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('clave', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('fk_area', models.ManyToManyField(to='Departamentos.Area')),
                ('fk_departamento', models.ForeignKey(to='Departamentos.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('codigo_udg', models.CharField(max_length=9, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.CharField(max_length=5, serialize=False, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_edif',
            field=models.ForeignKey(to='Departamentos.Edificio'),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_materia',
            field=models.ForeignKey(to='Departamentos.Materia'),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_profesor',
            field=models.ForeignKey(to='Departamentos.Profesor'),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_secc',
            field=models.ForeignKey(to='Departamentos.Seccion'),
        ),
        migrations.AddField(
            model_name='aula',
            name='fk_edif',
            field=models.ForeignKey(to='Departamentos.Edificio'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_departamento',
            field=models.ForeignKey(to='Departamentos.Departamento'),
        ),
    ]
