from django.http import HttpResponse
from jinja2 import TemplateSyntaxError
from urllib.parse import quote
from .models import Step, Stage, ReportTemplate
from .serializers import ReservistsTemplateSerializer
from docxtpl import DocxTemplate
from datetime import date
from .settings import MEDIA_ROOT
from os import path
import io

DOCX_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def make(request, stage_id, template_id):
    template = ReportTemplate.objects.get(id=template_id)
    stage = Stage.objects.get(id=stage_id)
    reservists = stage.reservists.all()
    context = {
        'stage': stage,
        'year': date.today().year,
        'dataset': ReservistsTemplateSerializer(reservists, many=True, context={'stage': stage}).data
    }

    import lxml
    try:
        report = DocxTemplate(path.join(MEDIA_ROOT, template.template_file.url))
        report.render(context)
    except TemplateSyntaxError as e:
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
