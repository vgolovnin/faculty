from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.core.mail import send_mass_mail
from smtplib import SMTPException
import json
from ..models import Reservist, Stage, Participation
from .settings import *



def preview(request, participation_id):
  try:
    participation = Participation.objects.get(id=participation_id)
  except Participation.DoesNotExist:
    pass

  ((subject, text, sender, recp),) = _render((participation,))

  return JsonResponse({
    'subject': subject,
    'text': text,
    'from': EMAIL_HOST_USER,
    'to': recp[0]
  })

def send_reminder(request):
  mail_info = json.loads(request.body.decode('utf-8'))
  error = ''
  count = 0

  try:
    count = _send(   ((mail_info['subject'], mail_info['text'], DEFAULT_FROM_EMAIL, [mail_info['to']]),)     )
  except Exception as err:
    error = str(err)

  return JsonResponse({
    'count': count,
    'error': error
  })

def deadline_reminder(participations):
  return _send(_render(participations))


def _send(datatuple):
  return send_mass_mail(datatuple)

def _render(participations):
  template = get_template('reminder.tpl.txt')
  return tuple(map(lambda p: (EMAIL_SUBJECT_PREFIX,
    template.render({
    'name': ' '.join(p.reservist.name.split()[1:]),
    'stage': p.stage.stageset.name,
    'deadline': p.stage.deadline,
  }), DEFAULT_FROM_EMAIL, [p.reservist.email]), participations))

