from django.shortcuts import render
from .models import Reservist, Status
from rest_framework import viewsets
from .serializers import *


def index(request):
    return render(request, 'index.html')

def reports(request):
    return render(request, 'reports.html')


class ReservistsViewSet(viewsets.ModelViewSet):
    serializer_class = ReservistsWebSerializer

    def get_queryset(self, pk=None):
        queryset = Reservist.objects.filter(category__isnull=False).select_related('category', 'status', 'department').all()
        return queryset


class ReportsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportsSerializer
    queryset = Stage.objects.all()

