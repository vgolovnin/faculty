# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 00:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0040_auto_20170413_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='reminder',
            field=models.DurationField(default=datetime.timedelta(3), null=True),
        ),
    ]
