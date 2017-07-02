from django.http import HttpResponseRedirect, JsonResponse
from django.template import Context, Template
from .models import Reservist, Stage, Participation
from django.core.mail import send_mail

from .settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_SUBJECT_PREFIX

MAIL_TEMPLATE = """Здравствуйте, {{ name }}!
Крайний срок по этапу {{ stage }} наступает {{ deadline }}
Пожалуйста, примите во внимание.


{{ signature }}
"""

MAIL_FROM = EMAIL_HOST_USER + '@' + EMAIL_HOST


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

