# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0004_auto_20150723_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='jefeDep',
        ),
    ]
