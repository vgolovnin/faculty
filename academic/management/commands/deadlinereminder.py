# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from academic.models import Reservist, Participation
from academic.mailer import reminders
from django.db.models import F
import datetime
from unidecode import unidecode


class Command(BaseCommand):
  help = 'Send emails to remind about deadlines'

  def handle(self, *args, **options):
    today = datetime.date.today()
    participations = Participation.objects.filter(stage__deadline__gt=today, stage__deadline__lte=today+F('reminder')) \
    .exclude(reminder=None).exclude(step__is_final=True)

    count = reminders.deadline_reminder(participations)
    print('DEADLINE', today, count)