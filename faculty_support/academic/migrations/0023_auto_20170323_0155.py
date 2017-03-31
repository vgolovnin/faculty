# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 22:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0022_reservist_personal_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_info', models.TextField()),
                ('quota', models.IntegerField(default=4)),
                ('dept_code', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservist',
            name='position',
            field=models.CharField(default='Сотрудник', max_length=200),
        ),
        migrations.AlterField(
            model_name='reservist',
            name='birthday',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='reservist',
            name='personal_page',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='reservist',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.Department'),
        ),
    ]