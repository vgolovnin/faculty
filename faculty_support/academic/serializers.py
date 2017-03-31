from .models import Reservist, Status, Stage
from rest_framework import serializers
from django.core.urlresolvers import reverse
import os


class StagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        read_only_fields = ('name', 'deadline', 'template')
        fields = ('name', 'deadline', 'done', 'id', 'template')

    done = serializers.BooleanField()
    id = serializers.IntegerField()
    template = serializers.SerializerMethodField()

    def get_template(self, obj):
        if obj.template_file:
            return os.path.basename(obj.template_file.url)
        else:
            return None


class ReservistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservist
        fields = ('name', 'category', 'status', 'department', 'position', 'experience',)

    category = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    department = serializers.StringRelatedField()


class ReservistsTemplateSerializer(ReservistsSerializer):
    class Meta:
        model = Reservist
        fields = ReservistsSerializer.Meta.fields +\
                 ('birthday',)

    department = serializers.SlugRelatedField('full_name', read_only=True)
    birthday = serializers.SerializerMethodField()

    def get_birthday(self, obj):
        return obj.birthday.strftime("%d.%m.%Y")


class ReservistsWebSerializer(ReservistsSerializer):
    class Meta:
        model = Reservist
        fields = ReservistsSerializer.Meta.fields +\
                 ('url', 'admin_url', 'stages', 'personal_page', 'email', 'phd')

    admin_url = serializers.SerializerMethodField()
    phd = serializers.SerializerMethodField()
    stages = StagesSerializer(many=True)

    def get_admin_url(self, obj):
        return reverse('admin:academic_reservist_change', args=[obj.id])

    def get_phd(self, obj):
        if obj.phd is None:
            return "Нет"
        else:
            return "Да, получена " + obj.phd.strftime("%d.%m.%Y")

    def update(self, instance, validated_data):
        for stage_data in validated_data.pop('stages'):
            stage = Stage.objects.get(id=stage_data['id'])
            if stage_data['done']:
                instance.current_stages.add(stage)
            else:
                instance.current_stages.remove(stage)

        return instance
