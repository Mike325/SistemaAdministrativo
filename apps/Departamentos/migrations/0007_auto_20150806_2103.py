# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Departamentos', '0006_auto_20150803_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='contrato',
            name='fk_tipocont',
            field=models.ForeignKey(blank=True, to='Departamentos.TipoContrato', null=True),
        ),
    ]
