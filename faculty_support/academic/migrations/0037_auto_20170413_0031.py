# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0036_daterequirment'),
    ]

    operations = [
        migrations.CreateModel(
            name='StageSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
        ),
        migrations.RemoveField(
            model_name='stage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='name',
        ),
        migrations.AddField(
            model_name='participation',
            name='reminder',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='reminder',
            field=models.DurationField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='daterequirment',
            unique_together=set([('field', 'stage')]),
        ),
        migrations.AddField(
            model_name='stage',
            name='stageset',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='academic.StageSet'),
            preserve_default=False,
        ),
    ]
