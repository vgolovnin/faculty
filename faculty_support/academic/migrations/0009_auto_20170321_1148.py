# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0008_reservist_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservist',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
