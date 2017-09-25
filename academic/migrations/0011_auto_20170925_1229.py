# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-25 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0010_auto_20170925_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='stageset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='academic.StageSet'),
        ),
    ]
