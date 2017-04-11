from .models import Reservist, Department, Stage, Step, Participation
from rest_framework import serializers
from django.core.urlresolvers import reverse
import os


class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ('id', 'name')


class StagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        read_only_fields = ('name', 'deadline', 'admin_url', 'steps')
        fields = ('name', 'deadline', 'id', 'admin_url', 'steps')

    steps = StepsSerializer(many=True, read_only=True)
    admin_url = serializers.SerializerMethodField()
    id = serializers.IntegerField()

    def get_admin_url(self, obj):
        return reverse('admin:academic_stage_change', args=[obj.id])


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
                 ('birthday',)

    department = DepartmentSerializer()
    birthday = serializers.SerializerMethodField()
    phd = serializers.SerializerMethodField()

    def get_birthday(self, obj):
        return obj.birthday.strftime("%d.%m.%Y")

    def get_phd(self, obj):
            return "Нет" if obj.phd is None else "Да"

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ('stage', 'step_selected')

    stage = StagesSerializer()
    step_selected = serializers.PrimaryKeyRelatedField(source='step', queryset=Step.objects.all())

class ReservistsWebSerializer(ReservistsSerializer):
    class Meta:
        model = Reservist
        fields = ReservistsSerializer.Meta.fields +\
                 ('url', 'admin_url', 'personal_page', 'email', 'participations')

    admin_url = serializers.SerializerMethodField()
    phd = serializers.SerializerMethodField()
    participations = ParticipationSerializer(many=True)


    @staticmethod
    def get_admin_url(obj):
        return reverse('admin:academic_reservist_change', args=[obj.id])

    @staticmethod
    def get_phd(obj):
        if obj.phd is None:
            return "Нет"
        else:
            return "Да, получена " + obj.phd.strftime("%d.%m.%Y")

    def update(self, instance, validated_data): # todo validate
        for participation_data in validated_data.pop('participations'):
            print(participation_data)
            p = Participation.objects.get(reservist=instance,
                                          stage=Stage.objects.get(id=participation_data['stage']['id']))
            p.step = participation_data['step']
            p.save()

        return instance
