# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Historicos', '0002_registro_fechahoramodificacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registro',
            name='fechaModificacion',
        ),
        migrations.RemoveField(
            model_name='registro',
            name='horaModificacion',
        ),
    ]
