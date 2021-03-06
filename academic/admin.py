from django import forms
from django.contrib import admin
import datetime
from .models import *

admin.site.site_header = 'Академический кадровый резерв'


class ReservistAdminForm(forms.ModelForm):
    class Meta:
        model = Reservist
        fields = '__all__'

    class Media:
        js = ('academic_admin.js',)

    def __init__(self, *args, **kwargs):
        super(ReservistAdminForm, self).__init__(*args, **kwargs)
        self.fields['degree'].empty_label = "Нет"

    def clean(self):
        if (self.cleaned_data.get('degree') is not None) and self.cleaned_data.get('phd') is None:
            raise forms.ValidationError({'phd': "Это поле обязательно."})
        return self.cleaned_data


@admin.register(Reservist)
class ReservistAdmin(admin.ModelAdmin):
    form = ReservistAdminForm
    fieldsets = [
        ('Личные данные', {'fields': (('name', 'personal_page'), ('email', 'birthday'), 'degree', 'phd')}),
        ('Основное место работы', {'fields': (('position', 'department', 'hse'),)}),
        ('Участие в программе', {'fields': (('category', 'status'),)}),
        (None, {'fields': ('comment',)})
    ]

    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)
        reservists = Reservist.objects.all()
        for res in reservists:
            res.update_participation()


class StepAdminInline(admin.TabularInline):
    model = Step
    fields = ('name', 'is_final')
    min_num = 2


class DateRequirmentAdminInline(admin.TabularInline):
    model = DateRequirment
    fields = ('field', 'threshold_min', 'threshold_max', 'status', 'description')


class ReportTemplateAdminInline(admin.TabularInline):
    model = ReportTemplate
    fields = ('name', 'template_file')


class ReminderDurationField(forms.DurationField):
    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            return value.days
        return value

    def to_python(self, value):
        try:
            return datetime.timedelta(days=int(value))
        except:
            raise forms.ValidationError("Укажите целое число дней") 


class StageForm(forms.ModelForm):
    reminder = ReminderDurationField()
    class Meta:
        model = Stage
        fields = '__all__'


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    form = StageForm
    class Media:
        css = {'all': ('academic_admin.css',)}

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }


    fieldsets = [
        (None, {'fields': ('stageset', 'stagename', 'deadline', 'reminder')}),
        ('Участники этапа', {'fields': (('categories', 'departments'),), 'classes': ('fields-multiple',)}),
        ('Данные шаблона', {'fields': (('name_by', 'name_to'), ('manager_position', 'manager_signature')) ,
                            'classes': ('collapse',)})
    ]

    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)
        reservists = Reservist.objects.all()
        for res in reservists:
            res.update_participation()


class QuotaAdminInline(admin.TabularInline):
    model = Quota
    fields = ('category', 'qty')

@admin.register(StageSet)
class StageSetAdmin(admin.ModelAdmin):
    inlines = (StepAdminInline, ReportTemplateAdminInline)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (DateRequirmentAdminInline,)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = (QuotaAdminInline,)

admin.site.register(Position)
admin.site.register(Degree)

admin.site.register(Status)


