from django.conf.urls import url, include

from . import views, reports

from rest_framework import routers
from .views import ReservistsViewSet

router = routers.DefaultRouter()
router.register(r'reserve', ReservistsViewSet, base_name='reservist')


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^reports/dean$', reports.make, {'step_id': 10}),
    url(r'^reports/ami$', reports.make, {'step_id': 7}),
    url(r'^reports/step/(?P<step_id>[0-9]+)$', reports.make)
]

