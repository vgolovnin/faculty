from django.conf.urls import url, include
from django.contrib import admin
from . import views, reports
# from .views import ReportsViewSet, ParticipationsViewSet
from .mailer import reminders
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', views.ReportsViewSet, base_name='report')
router.register(r'participation', views.ParticipationsViewSet, base_name='participation')


urlpatterns = [
    url(r'^$', views.vue),
    url(r'^reports/$', views.vue),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^reports/stage/(?P<stage_id>[0-9]+)/template/(?P<template_id>[0-9]+)$', reports.make),
    url(r'^mailers/preview/(?P<participation_id>[0-9]+)$', reminders.preview),
    url(r'^mailers/send_reminder$', reminders.send_reminder)
]

