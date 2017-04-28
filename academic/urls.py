from django.conf.urls import url, include
from django.contrib import admin
from . import views, reports, reminders
from rest_framework import routers
from .views import ReservistsViewSet, ReportsViewSet


router = routers.DefaultRouter()
router.register(r'reserve', ReservistsViewSet, base_name='reservist')
router.register(r'reports', ReportsViewSet, base_name='report')


urlpatterns = [
    url(r'^$', views.index),
    url(r'^reports/$', views.index),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^reminders/reservist/(?P<reservist_id>[0-9]+)/stage/(?P<stage_id>[0-9]+)$', reminders.mail),
    url(r'^reports/stage/(?P<stage_id>[0-9]+)/template/(?P<template_id>[0-9]+)$', reports.make)
]

