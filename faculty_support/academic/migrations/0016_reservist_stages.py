# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0015_auto_20170322_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservist',
            name='stages',
            field=models.ManyToManyField(to='academic.Stage'),
        ),
    ]