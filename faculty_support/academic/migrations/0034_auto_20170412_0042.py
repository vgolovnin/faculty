# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 21:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0033_auto_20170404_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Должность')),
            ],
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'verbose_name': 'Шаг', 'verbose_name_plural': 'Шаги'},
        ),
        migrations.AddField(
            model_name='reservist',
            name='stages',
            field=models.ManyToManyField(through='academic.Participation', to='academic.Stage'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='reservist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to='academic.Reservist'),
        ),
        migrations.AlterField(
            model_name='reservist',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Position'),
        ),
        migrations.AlterField(
            model_name='reservist',
            name='steps',
            field=models.ManyToManyField(related_name='reservists', through='academic.Participation', to='academic.Step'),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('reservist', 'stage')]),
        ),
        migrations.AlterUniqueTogether(
            name='step',
            unique_together=set([('name', 'stage')]),
        ),
    ]