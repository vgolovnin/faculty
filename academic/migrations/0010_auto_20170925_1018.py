# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-25 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0009_daterequirment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daterequirment',
            name='description',
            field=models.CharField(blank=True, max_length=256, verbose_name='Описание'),
        ),
    ]
