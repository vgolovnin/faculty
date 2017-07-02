from django.http import HttpResponse
from jinja2 import TemplateSyntaxError
from urllib.parse import quote
import jinja2
import pymorphy2
from .models import Step, Stage, ReportTemplate
from .serializers import ReservistsTemplateSerializer
from docxtpl import DocxTemplate
from datetime import date
from .settings import MEDIA_ROOT
from os import path
import io

DOCX_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'



def inflect(dept, transform='gent'):
    morph = pymorphy2.MorphAnalyzer()

    words = dept.split()

    inflected = []
    inflect_done = False

    for word in words:
        t_word = ''
        if not inflect_done:
            p = morph.parse(word)[0]
            t_word = pymorphy2.shapes.restore_capitalization(p.inflect({transform}).word, word)
            inflect_done = 'NOUN' in p.tag
        else:
            t_word = word
        inflected.append(t_word)

    return ' '.join(inflected)


def make(request, stage_id, template_id):
    template = ReportTemplate.objects.get(id=template_id)
    stage = Stage.objects.get(id=stage_id)
    reservists = stage.reservists.all()
    context = {
        'stage': stage,
        'year': date.today().year,
        'dataset': ReservistsTemplateSerializer(reservists, many=True, context={'stage': stage}).data
    }

    jinja_env = jinja2.Environment()
    jinja_env.filters['inflect'] = inflect

    import lxml
    try:
        report = DocxTemplate(path.join(MEDIA_ROOT, template.template_file.url))
        report.render(context, jinja_env)
    except jinja2.TemplateSyntaxError as e:
        return HttpResponse("{'error': '" + e.message + "', 'description':" +
                            "'Возникла проблема при обработке шаблона'}")
    except lxml.etree.XMLSyntaxError:
        return HttpResponse("{'error': 'XMLSyntaxError', 'description':" +
                            "'Возникла проблема при обработке шаблона'}")
    else:
        filename = stage.stagename + ' (' + template.name + ').docx'
        response = HttpResponse(content_type=DOCX_TYPE)
        response['Content-Disposition'] = 'attachment; filename=\'%s\'' % quote(filename, '()')
        report.save(response)
        return response
