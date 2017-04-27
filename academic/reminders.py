from django.http import HttpResponseRedirect
from django.template import Context, Template
from .models import Reservist, Stage
from django.core.mail import send_mail

MAIL_TEMPLATE = """
Здравствуйте, {{ name }}!
У Вас не готова {{ stage }}.
Заполните, пожалуйста, до {{ deadline }}

{{ signature }}
"""

MAIL_FROM = "leo@mathtech.ru"


def mail(request, reservist_id, stage_id):
    reservist = Reservist.objects.get(id=reservist_id)
    stage = Stage.objects.get(id=stage_id)
    with open('email_templates/signature.txt', 'rt') as signature:
        send_mail("Напоминание от академического резерва", Template(MAIL_TEMPLATE).render(Context(
        {'name': ' '.join(reservist.name.split()[1:]),
         'stage': stage.stageset.name,
         'deadline': stage.deadline,
         'signature': ''.join(signature.readlines())})), MAIL_FROM, (reservist.email,))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))