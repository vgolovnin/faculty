# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 04:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0012_stage_statuses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Category')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Status')),
            ],
        ),
        migrations.RemoveField(
            model_name='stage',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='statuses',
        ),
        migrations.AddField(
            model_name='stage',
            name='section',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='academic.Section'),
            preserve_default=False,
        ),
    ]