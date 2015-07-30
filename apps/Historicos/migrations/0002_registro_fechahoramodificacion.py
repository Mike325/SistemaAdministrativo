# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Historicos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='fechaHoraModificacion',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 30, 5, 47, 3, 264793, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]