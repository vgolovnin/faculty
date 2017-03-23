from django.db import models

from django.db.models import When, Case, Count, Value
from datetime import date
from dateutil import relativedelta

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


class Stage(models.Model):
    name = models.CharField('Этап', max_length=200)
    description = models.TextField('Описание', blank=True)
    deadline = models.DateField('Крайний срок')
    categories = models.ManyToManyField(Category)
    statuses = models.ManyToManyField(Status)
    template_file = models.FileField('Файд шаблона', null=True, blank=True, upload_to='report_templates')

    class Meta:
        verbose_name = "Этап участия"
        verbose_name_plural = "Этапы участия"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.TextField()
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


class Reservist(models.Model):
    class Meta:
        verbose_name = "Участник программы"
        verbose_name_plural = "Участники программы"

    name = models.CharField(max_length=200)
    email = models.EmailField()
    comment = models.TextField(blank=True, null=True)
    personal_page = models.URLField(blank=True)
    birthday = models.DateField('Дата рождения')
    category = models.ForeignKey(Category, null=True)
    status = models.ForeignKey(Status, null=True, related_name='reservists')
    stages = models.ManyToManyField(Stage, related_name='reservists', blank=True, editable=False)
    department = models.ForeignKey(Department, verbose_name="Основное место работы", null=True)
    position = models.CharField(max_length=200, verbose_name="Должность", default="Сотрудник")
    phd = models.DateField('Дата получения учёной степени (если есть)', null=True, blank=True)
    hse = models.DateField('Дата начала работы в ВШЭ')

    def current_stages(self):
        return Stage.objects.filter(categories=self.category, statuses=self.status)\
            .annotate(done=Count(Case(When(reservists=self, then=Value(True))), distinct=True))\
            .order_by('deadline')

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

    def __str__(self):
        return self.name
