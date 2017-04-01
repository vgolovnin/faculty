from django.conf.urls import url, include

from . import views, reports

from rest_framework import routers
from .views import ReservistsViewSet

router = routers.DefaultRouter()
router.register(r'reserve', ReservistsViewSet, base_name='reservist')


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^reports/dean$', reports.make),
    url(r'^reports/stage/(?P<stage_id>[0-9]+)$', reports.make)
]

