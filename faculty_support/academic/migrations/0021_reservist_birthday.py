# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0020_remove_reservist_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservist',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
    ]
