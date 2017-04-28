from .models import Reservist, Department, Stage, Status, Step, Participation, DateRequirment, ReportTemplate
from rest_framework import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import date


class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ('id', 'name', 'is_final')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('name', 'description')


class StagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        read_only_fields = ('name', 'deadline', 'admin_url', 'steps', 'stagename', 'warning')
        fields = ('name', 'deadline', 'id', 'admin_url', 'steps', 'stagename', 'warning')

    steps = StepsSerializer(many=True, read_only=True)
    admin_url = serializers.SerializerMethodField()
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    warning = serializers.SerializerMethodField()

    def get_warning(self, obj):
        return not (obj.reminder is None or (date.today() - obj.deadline) < obj.reminder)

    def get_name(self, obj):
        return obj.stageset.name

    def get_admin_url(self, obj):
        return reverse('admin:academic_stage_change', args=[obj.id]) \
        if self.context['request'].user.has_perm('academic.change_stage') else None


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name', 'full_name')


class ReservistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservist
        fields = ('name', 'category', 'status', 'department', 'position', 'experience', 'phd')

    category = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    position = serializers.StringRelatedField()


class ReservistsTemplateSerializer(ReservistsSerializer):
    class Meta:
        model = Reservist
        fields = ReservistsSerializer.Meta.fields +\
                 ('birthday', 'step')

    department = DepartmentSerializer()
    birthday = serializers.SerializerMethodField()
    phd = serializers.SerializerMethodField()
    status = StatusSerializer()
    step = serializers.SerializerMethodField()

    def get_step(self, obj):
        return Participation.objects.get(reservist=obj, stage=self.context['stage']).step.name

    def get_birthday(self, obj):
        return obj.birthday.strftime("%d.%m.%Y")

    def get_phd(self, obj):
            return obj.degree.name if obj.degree is not None else "Нет"


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ('stage', 'step_selected', 'disabled')

    disabled = serializers.SerializerMethodField()
    stage = StagesSerializer()
    step_selected = serializers.PrimaryKeyRelatedField(source='step', queryset=Step.objects.all())

    def get_disabled(self, obj):
        return not self.context['request'].user.is_authenticated()


class ReservistsWebSerializer(ReservistsSerializer):
    class Meta:
        model = Reservist
        fields = ReservistsSerializer.Meta.fields +\
                 ('id', 'url', 'admin_url', 'personal_page', 'email', 'participations', 'warnings', 'age')

    admin_url = serializers.SerializerMethodField()
    phd = serializers.SerializerMethodField()
    participations = ParticipationSerializer(many=True)
    warnings = serializers.SerializerMethodField()

    @staticmethod
    def get_warnings(obj):
        datereq = DateRequirment.objects.filter(stage__reservist=obj)
        phdreq = datereq.filter(field='phd')
        dept = obj.department
        return {
            'department': dept.reservists.filter(category__is_quoted=True).count() > dept.quota,
            'hse': datereq.filter(Q(field='hse') & (Q(threshold_min__gte=obj.hse) |
                                                    Q(threshold_max__lte=obj.hse))).count() > 0,
            'phd': phdreq.count() > 0 and (obj.degree is None or phdreq.filter(Q(threshold_min__gte=obj.phd) |
                                                    Q(threshold_max__lte=obj.phd)).count() > 0),
            'age': datereq.filter(Q(field='bth') & (Q(threshold_min__gte=obj.birthday) |
                                                    Q(threshold_max__lte=obj.birthday))).count() > 0,
        }

    @staticmethod
    def get_admin_url(obj):
        return reverse('admin:academic_reservist_change', args=[obj.id])

    @staticmethod
    def get_phd(obj):
        if obj.degree is None:
            return "Нет"
        else:
            return obj.degree.short_name + " (" + obj.phd.strftime("%d.%m.%Y") + ")"

    def update(self, instance, validated_data): # todo validate
        for participation_data in validated_data.pop('participations'):
            p = Participation.objects.get(reservist=instance,
                                          stage=Stage.objects.get(id=participation_data['stage']['id']))
            p.step = participation_data['step']
            p.save()

        return instance


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ('id', 'name')


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('stageset', 'url', 'name', 'stagename', 'templates')

    url = serializers.SerializerMethodField()
    stagename = serializers.SerializerMethodField()
    templates = serializers.SerializerMethodField()
    stageset = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_templates(self, obj):
        serializer = TemplatesSerializer(obj.stageset.templates, many=True)
        return serializer.data

    def get_url(self, obj):
        return "/reports/stage/" + str(obj.id)

    def get_stagename(self, obj):
        return obj.stagename