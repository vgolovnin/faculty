# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0032_reporttemplate_step'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporttemplate',
            name='step',
        ),
        migrations.AddField(
            model_name='step',
            name='template_consolidated',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='step',
            name='template_file',
            field=models.FileField(blank=True, null=True, upload_to='report_templates', verbose_name='Шаблон отчёта'),
        ),
        migrations.DeleteModel(
            name='ReportTemplate',
        ),
    ]