# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('tipo', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('codigo', models.CharField(unique=True, max_length=9)),
                ('nombre', models.CharField(max_length=50, blank=True)),
                ('apellidos', models.CharField(max_length=50, blank=True)),
                ('rol', models.ForeignKey(to='Usuarios.Rol')),
            ],
        ),
    ]
