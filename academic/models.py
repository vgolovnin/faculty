from datetime import date, timedelta

import os
from dateutil import relativedelta
from django.db import models
from .settings import BASE_DIR


class Department(models.Model):
    name = models.CharField('Название', max_length=200)
    short_name = models.CharField('Сокращённое название', max_length=200, null=True)
    quota = models.IntegerField(default=4, verbose_name="Квота на участие")
    parent = models.ForeignKey('Department', verbose_name="Вышестоящее подразделение", related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    @property
    def full_name(self):
        if self.parent is None:
            return self.name
        else:
            return "%s, %s" % (self.parent.full_name, self.name)

    def __str__(self):
        return self.short_name if self.short_name else self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField('Описание', blank=True)
    is_quoted = models.BooleanField('Квотирование участников', default=True)

    class Meta:
        verbose_name = "Конкурсная категория"
        verbose_name_plural = "Конкурсные категории"

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "Статус участия"
        verbose_name_plural = "Статусы участия"

    def __str__(self):
        return self.name

DATE_CHOICE = (
    ('hse', "Дата начала работы"),
    ('phd', "Дата присвоения учёной степени"),
    ('bth', "Дата рождения")
)


class DateRequirment(models.Model):
    class Meta:
        unique_together = ('field', 'category', 'status')
        verbose_name = "Формальное требование"
        verbose_name_plural = "Формальные требования"

    field = models.CharField(max_length=3, choices=DATE_CHOICE, verbose_name="Тип")
    threshold_min = models.DateField(null=True, blank=True, verbose_name="Минимум")
    threshold_max = models.DateField(null=True, blank=True, verbose_name="Максимум")
    description = models.CharField('Описание', max_length=256, blank=True)
    category = models.ForeignKey('Category')
    status = models.ForeignKey('Status')


class StageSet(models.Model):
    class Meta:
        verbose_name = "Группа этапов"
        verbose_name_plural = "Группы этапов"

    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    statuses = models.ManyToManyField(Status, verbose_name="Статусы участников")

    def __str__(self):
        return self.name


class Stage(models.Model):
    class Meta:
        verbose_name = "Этап участия"
        verbose_name_plural = "Этапы участия"
        ordering = ('deadline',)

    stageset = models.ForeignKey(StageSet)
    stagename = models.CharField(max_length=200)
    deadline = models.DateField('Крайний срок')
    categories = models.ManyToManyField(Category, verbose_name="Конкурсные категории")
    departments = models.ManyToManyField(Department, verbose_name="Подразделения", limit_choices_to={'children': None})
    reminder = models.DurationField(null=True, default=timedelta(days=3))
    reservists = models.ManyToManyField('Reservist', through='Participation')
    name_by = models.CharField(max_length=200, blank=True)
    name_to = models.CharField(max_length=200, blank=True)
    manager_position = models.CharField(max_length=200, blank=True)
    manager_signature = models.CharField(max_length=200, blank=True)

    @property
    def statuses(self):
        return self.stageset.statuses

    @property
    def steps(self):
        return self.stageset.steps

    @property
    def name(self):
        return self.stageset.name

    def __str__(self):
        return self.stagename


class ReportTemplate(models.Model):
    class Meta:
        verbose_name = "Шаблон отчёта"
        verbose_name_plural = "Шаблоны отчётов"
        permissions = (
            ('reports', "Can make reports"),
        )

    name = models.CharField(max_length=200, verbose_name="Название")
    template_file = models.FileField('Файл шаблона', null=True, blank=True, upload_to='report_templates')
    stageset = models.ForeignKey(StageSet, related_name='templates')

    def __str__(self):
        return self.name


class Step(models.Model):
    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"
        unique_together = ('name', 'stageset')

    name = models.CharField('Название', max_length=200)
    stageset = models.ForeignKey(StageSet, related_name='steps')
    is_final = models.BooleanField('Является финальным', default=False)

    def __str__(self):
        return self.name


class Participation(models.Model):
    class Meta:
        unique_together = ('reservist', 'stage')

    reservist = models.ForeignKey('Reservist', related_name='participations')
    stage = models.ForeignKey('Stage')
    step = models.ForeignKey('Step')
    reminder = models.DurationField(null=True)


class Position(models.Model):
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    name = models.CharField(max_length=200, verbose_name='Должность')

    def __str__(self):
        return self.name


class Degree(models.Model):
    class Meta:
        verbose_name = "Учёная степень"
        verbose_name_plural = "Учёные степени"

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)

    def __str__(self):
        return self.short_name


class Reservist(models.Model):
    class Meta:
        verbose_name = "Участник программы"
        verbose_name_plural = "Участники программы"

    name = models.CharField(max_length=200, verbose_name='ФИО')
    email = models.EmailField()
    comment = models.TextField('Комментарий', blank=True, null=True)
    personal_page = models.URLField(blank=True, verbose_name='Личная страница')
    birthday = models.DateField('Дата рождения')
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name="Конкурсная категория")
    status = models.ForeignKey(Status, null=True, related_name='reservists', verbose_name="Статус участия")
    steps = models.ManyToManyField(Step, through=Participation, related_name='reservists')
    stages = models.ManyToManyField(Stage, through=Participation)
    department = models.ForeignKey(Department, related_name='reservists', verbose_name="Подразделение", null=True)
    position = models.ForeignKey(Position, verbose_name="Должность")
    degree = models.ForeignKey(Degree, null=True, blank=True, default=None, verbose_name="Учёная степень")
    phd = models.DateField('Дата получения учёной степени', null=True, blank=True)
    hse = models.DateField('Дата начала работы в ВШЭ')

    @property
    def experience(self):
        rd = relativedelta.relativedelta(date.today(), self.hse)
        experience = ""
        if rd.years > 0:
            experience += "%d г." % rd.years
            if rd.months > 0:
                experience += " "
        if rd.months > 0:
            experience += "%d мес." % rd.months
        return experience

    @property
    def age(self):
        rd = relativedelta.relativedelta(date.today(), self.birthday)
        return rd.years

    def update_participation(self):
        if self.category is not None:
            current_stages = self.category.stage_set.filter(stageset__statuses=self.status, departments=self.department).distinct().all()
            Participation.objects.filter(reservist=self).exclude(stage__in=current_stages).delete()

            for stage in current_stages:
                Participation.objects.get_or_create(reservist=self, stage=stage,
                                                   defaults={'step': stage.steps.first(),
                                                             'reminder': stage.reminder})

    def __str__(self):
        return self.name
