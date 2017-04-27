# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('is_quoted', models.BooleanField(default=True, verbose_name='Квотирование участников')),
            ],
            options={
                'verbose_name_plural': 'Конкурсные категории',
                'verbose_name': 'Конкурсная категория',
            },
        ),
        migrations.CreateModel(
            name='DateRequirment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(choices=[('hse', 'Дата начала работы'), ('phd', 'Дата присвоения учёной степени'), ('bth', 'Дата рождения')], max_length=3, verbose_name='Тип')),
                ('threshold_min', models.DateField(blank=True, null=True, verbose_name='Минимум')),
                ('threshold_max', models.DateField(blank=True, null=True, verbose_name='Максимум')),
            ],
            options={
                'verbose_name_plural': 'Формальные требования',
                'verbose_name': 'Формальное требование',
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Учёные степени',
                'verbose_name': 'Учёная степень',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('quota', models.IntegerField(default=4, verbose_name='Квота на участие')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='academic.Department', verbose_name='Вышестоящее подразделение')),
            ],
            options={
                'verbose_name_plural': 'Подразделения',
                'verbose_name': 'Подразделение',
            },
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reminder', models.DurationField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Должность')),
            ],
            options={
                'verbose_name_plural': 'Должности',
                'verbose_name': 'Должность',
            },
        ),
        migrations.CreateModel(
            name='ReportTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('template_file', models.FileField(blank=True, null=True, upload_to='report_templates', verbose_name='Файл шаблона')),
            ],
            options={
                'verbose_name_plural': 'Шаблоны отчётов',
                'permissions': (('reports', 'Can make reports'),),
                'verbose_name': 'Шаблон отчёта',
            },
        ),
        migrations.CreateModel(
            name='Reservist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('personal_page', models.URLField(blank=True, verbose_name='Личная страница')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('phd', models.DateField(blank=True, null=True, verbose_name='Дата получения учёной степени')),
                ('hse', models.DateField(verbose_name='Дата начала работы в ВШЭ')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.Category', verbose_name='Конкурсная категория')),
                ('degree', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.Degree', verbose_name='Учёная степень')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservists', to='academic.Department', verbose_name='Подразделение')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Position', verbose_name='Должность')),
            ],
            options={
                'verbose_name_plural': 'Участники программы',
                'verbose_name': 'Участник программы',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stagename', models.CharField(max_length=200)),
                ('deadline', models.DateField(verbose_name='Крайний срок')),
                ('reminder', models.DurationField(default=datetime.timedelta(3), null=True)),
                ('name_by', models.CharField(blank=True, max_length=200)),
                ('name_to', models.CharField(blank=True, max_length=200)),
                ('manager_position', models.CharField(blank=True, max_length=200)),
                ('manager_signature', models.CharField(blank=True, max_length=200)),
                ('categories', models.ManyToManyField(to='academic.Category', verbose_name='Конкурсные категории')),
                ('departments', models.ManyToManyField(to='academic.Department', verbose_name='Подразделения')),
                ('reservists', models.ManyToManyField(through='academic.Participation', to='academic.Reservist')),
            ],
            options={
                'ordering': ('deadline',),
                'verbose_name_plural': 'Этапы участия',
                'verbose_name': 'Этап участия',
            },
        ),
        migrations.CreateModel(
            name='StageSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name_plural': 'Группы этапов',
                'verbose_name': 'Группа этапов',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Статусы участия',
                'verbose_name': 'Статус участия',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('stageset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='academic.StageSet')),
            ],
            options={
                'verbose_name_plural': 'Шаги',
                'verbose_name': 'Шаг',
            },
        ),
        migrations.AddField(
            model_name='stageset',
            name='statuses',
            field=models.ManyToManyField(to='academic.Status', verbose_name='Статусы участников'),
        ),
        migrations.AddField(
            model_name='stage',
            name='stageset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.StageSet'),
        ),
        migrations.AddField(
            model_name='reservist',
            name='stages',
            field=models.ManyToManyField(through='academic.Participation', to='academic.Stage'),
        ),
        migrations.AddField(
            model_name='reservist',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservists', to='academic.Status', verbose_name='Статус участия'),
        ),
        migrations.AddField(
            model_name='reservist',
            name='steps',
            field=models.ManyToManyField(related_name='reservists', through='academic.Participation', to='academic.Step'),
        ),
        migrations.AddField(
            model_name='reporttemplate',
            name='stageset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='academic.StageSet'),
        ),
        migrations.AddField(
            model_name='participation',
            name='reservist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to='academic.Reservist'),
        ),
        migrations.AddField(
            model_name='participation',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Stage'),
        ),
        migrations.AddField(
            model_name='participation',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Step'),
        ),
        migrations.AddField(
            model_name='daterequirment',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Stage'),
        ),
        migrations.AlterUniqueTogether(
            name='step',
            unique_together=set([('name', 'stageset')]),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('reservist', 'stage')]),
        ),
        migrations.AlterUniqueTogether(
            name='daterequirment',
            unique_together=set([('field', 'stage')]),
        ),
    ]
