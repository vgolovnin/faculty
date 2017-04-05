from django.shortcuts import render
from .models import Reservist, Status
from rest_framework import viewsets
from .serializers import *


def index(request):
    return render(request, 'index.html')


class ReservistsViewSet(viewsets.ModelViewSet):
    serializer_class = ReservistsWebSerializer

    def get_queryset(self, pk=None):
        queryset = Reservist.objects.select_related('category', 'status', 'department').all()
            #.prefetch_related('category__stage_set', 'status__stage_set', 'department__stage_set').all()
        return queryset