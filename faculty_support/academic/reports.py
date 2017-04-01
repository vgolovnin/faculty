from django.http import HttpResponse
from django.views.static import serve
from jinja2 import TemplateSyntaxError

from .models import Stage, Reservist
from .serializers import ReservistsTemplateSerializer
from docxtpl import DocxTemplate
from datetime import date
from tempfile import gettempdir


DOCX_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def make(request, stage_id=5):
    stage = Stage.objects.get(id=stage_id)
    reservists = stage.reservists.all()
    context = {
        'year': date.today().year,
        'dataset': ReservistsTemplateSerializer(reservists, many=True).data
    }

    import lxml
    try:
        report = DocxTemplate(stage.template_file.url)
        report.render(context)
    except TemplateSyntaxError as e:
        return HttpResponse("{'error': '" + e.message + "', 'description':" +
                            "'Возникла проблема при обработке шаблона'}")
    except lxml.etree.XMLSyntaxError:
        return HttpResponse("{'error': 'XMLSyntaxError', 'description':" +
                            "'Возникла проблема при обработке шаблона'}")
    else:
        FILENAME = 'report.docx'
        FILEDIR = gettempdir()
        report.save(FILEDIR + '/' + FILENAME)
        return serve(request, FILENAME, FILEDIR)
