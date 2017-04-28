from django.http import HttpResponse
from django.views.static import serve
from jinja2 import TemplateSyntaxError

from .models import Step, Stage, ReportTemplate
from .serializers import ReservistsTemplateSerializer
from docxtpl import DocxTemplate
from datetime import date
from tempfile import gettempdir
from .settings import MEDIA_ROOT
from os import path

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
        filename = 'report_' + stage.stagename + '_' + template.name + '.docx'
        filedir = gettempdir()
        report.save(filedir + '/' + filename)
        return serve(request, filename, filedir)
