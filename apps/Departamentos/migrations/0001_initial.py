# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nick', models.CharField(unique=True, max_length=20, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Use solo caracteres alfanumericos (a-Z, 0-9).')])),
                ('nombre', models.CharField(max_length=120)),
                ('jefeDep', models.OneToOneField(null=True, blank=True, to='Usuarios.Usuario')),
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
            name='Horario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('hora_ini', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('L', models.BooleanField(default=False)),
                ('M', models.BooleanField(default=False)),
                ('I', models.BooleanField(default=False)),
                ('J', models.BooleanField(default=False)),
                ('V', models.BooleanField(default=False)),
                ('S', models.BooleanField(default=False)),
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
            name='fk_horarios',
            field=models.ManyToManyField(to='Departamentos.Horario', blank=True),
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
