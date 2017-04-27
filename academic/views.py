from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .serializers import *


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/admin/login/')
def reports(request):
    return render(request, 'reports.html')


class ReservistsViewSet(viewsets.ModelViewSet):
    serializer_class = ReservistsWebSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self, pk=None):
        queryset = Reservist.objects.filter(category__isnull=False)\
            .select_related('category', 'status', 'department').all()
        return queryset


class ReportsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportsSerializer
    queryset = Stage.objects.filter(stageset__templates__isnull=False).order_by('deadline')

