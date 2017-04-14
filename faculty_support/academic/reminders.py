from django.http import HttpResponseRedirect
from django.template import Context, Template
from .models import Reservist, Stage
from django.core.mail import send_mail

MAIL_TEMPLATE = """
Здравствуйте, {{ name }}!
У Вас не готова {{ stage }}.
Заполните, пожалуйста, до {{ deadline }}

-- Sincerely Yours, Leonid W. Dworzanski.
Coordinator of High Potential group of Faculty of Computer Science
National Research University Higher School of Economics
mailto: leo@mathtech.ru
"""

MAIL_FROM = "leo@mathtech.ru"


def mail(request, reservist_id, stage_id):
    reservist = Reservist.objects.get(id=reservist_id)
    stage = Stage.objects.get(id=stage_id)
    send_mail("Напоминание от академического резерва", Template(MAIL_TEMPLATE).render(Context(
        {'name': ' '.join(reservist.name.split()[1:]),
         'stage': stage.stageset.name,
         'deadline': stage.deadline })), MAIL_FROM, (reservist.email,))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))