# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 23:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0034_auto_20170412_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='reservist',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservists', to='academic.Department', verbose_name='Подразделение'),
        ),
        migrations.AddField(
            model_name='reservist',
            name='degree',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.Degree'),
        ),
    ]
