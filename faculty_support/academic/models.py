from datetime import date, datetime, timedelta
from dateutil import relativedelta
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200)
    manager_name = models.CharField(max_length=200)
    manager_email = models.EmailField()
    quota = models.IntegerField(default=4)
    parent = models.ForeignKey('Department', related_name='children', null=True, blank=True)

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
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField('Описание', blank=True)

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
    ('hse', "Начало работы"),
    ('phd', "Присвоение учёной степени"),
    ('bth', "Рождение")
)


class DateRequirment(models.Model):
    class Meta:
        unique_together = ('field', 'stage')

    field = models.CharField(max_length=3, choices=DATE_CHOICE, verbose_name="Дата")
    threshold_min = models.DateField(null=True, blank=True)
    threshold_max = models.DateField(null=True, blank=True)
    stage = models.ForeignKey('Stage')


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

    class Meta:
        verbose_name = "Этап участия"
        verbose_name_plural = "Этапы участия"

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

# RTL_DIR = '/home/andrey/faculty/faculty_support/report_templates'
RTL_DIR = 'report_templates'  # todo BASE_DIR

class ReportTemplate(models.Model):
    name = models.CharField(max_length=200)
    template_file = models.FileField('Шаблон отчёта', null=True, blank=True, upload_to=RTL_DIR)
    stageset = models.ForeignKey(StageSet, related_name='templates')

    def __str__(self):
        return self.name

class Step(models.Model):
    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"
        unique_together = ('name', 'stageset')

    name = models.CharField(max_length=200)
    stageset = models.ForeignKey(StageSet, related_name='steps')

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
    position = models.ForeignKey(Position)
    degree = models.ForeignKey(Degree, null=True, blank=True, default=None)
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
