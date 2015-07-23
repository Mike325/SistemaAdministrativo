# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('tipo', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(default=1, to='Usuarios.Rol'),
            preserve_default=False,
        ),
    ]
