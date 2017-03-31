from django import forms
from django.contrib import admin
from .models import *


class ReservistAdminForm(forms.ModelForm):
    class Meta:
        model = Reservist
        fields = '__all__'

    class Media:
        css = {'all': ('css/academic-admin.css',)}
        js = ('js/academic-admin.js',)

    def __init__(self, *args, **kwargs):
        super(ReservistAdminForm, self).__init__(*args, **kwargs)
        if self.instance.phd is not None:
            self.initial['degree'] = 'PHD'

    degree = forms.ChoiceField((('NO', 'Нет'), ('PHD', 'PHD/Кандидат наук'),), label='Учёная степень')

    def clean(self):
        if self.cleaned_data.get('degree') == 'PHD' and self.cleaned_data.get('phd') is None:
            raise forms.ValidationError({'phd': "Это поле обязательно."})
        return self.cleaned_data


@admin.register(Reservist)
class ReservistAdmin(admin.ModelAdmin):
    form = ReservistAdminForm
    fieldsets = [
        ('Личные данные', {'fields': (('name', 'personal_page'), ('email', 'birthday'), 'degree', 'phd')}),
        ('Основное место работы', {'fields': (('position', 'department', 'hse'),)}),
        ('Участие в программе', {'fields': ('category', 'status')}),
        (None, {'fields': ('comment',)})
    ]


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('css/academic-admin.css',)}

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }
    fieldsets = [
        (None, {'fields': (('name', 'deadline'),('description',))}),
        ('Участники этапа', {'fields': (('statuses', 'categories', 'departments'),), 'classes': ('fields-multiple',)}),
        ('Отчёты и уведомления', {'fields': ('template_file',)})
    ]


admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Department)
