from django.http import HttpResponseRedirect, JsonResponse
from django.template import Context, Template
from .models import Reservist, Stage, Participation
from django.core.mail import send_mail

from smtplib import SMTPException

from .settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_SUBJECT_PREFIX
import json

MAIL_TEMPLATE = """Здравствуйте, {{ name }}!
Крайний срок по этапу {{ stage }} наступает {{ deadline }}
Пожалуйста, примите во внимание.


{{ signature }}
"""

MAIL_FROM = EMAIL_HOST_USER #+ '@' + EMAIL_HOST


# def mail(request, reservist_id, stage_id):
#     reservist = Reservist.objects.get(id=reservist_id)
#     stage = Stage.objects.get(id=stage_id)
#     with open('mailer/signature.txt', 'rt') as signature:
#         send_mail("Напоминание от академического резерва", Template(MAIL_TEMPLATE).render(Context(
#         {'name': ' '.join(reservist.name.split()[1:]),
#          'stage': stage.stageset.name,
#          'deadline': stage.deadline,
#          'signature': ''.join(signature.readlines())})), MAIL_FROM, (reservist.email,))
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     
def send_reminder(request):
    mail_info = json.loads(request.body.decode('utf-8'))
    error = ''
    count = 0

    try:
        count = send_mail(mail_info['subject'], mail_info['text'], MAIL_FROM, [mail_info['to']])
    except SMTPException as err:
        error = str(err)

    return JsonResponse({
        'count': count,
        'error': error
    })

def get_mail(request, participation_id):
    participation = Participation.objects.get(id=participation_id)
    reservist = participation.reservist
    stage = participation.stage
    with open('academic/mailer/signature.txt', 'rt') as signature:
        mailtext = Template(MAIL_TEMPLATE).render(Context(
                    {'name': ' '.join(reservist.name.split()[1:]),
                     'stage': stage.stageset.name,
                     'deadline': stage.deadline,
                     'signature': ''.join(signature.readlines())}))
    return JsonResponse({
        'from': MAIL_FROM,
        'to': reservist.email,
        'subject': EMAIL_SUBJECT_PREFIX,
        'text': mailtext,
    })

