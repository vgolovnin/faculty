from django.shortcuts import render
from .models import Reservist, Status
from rest_framework import viewsets
from .serializers import *


def index(request):
    return render(request, 'index.html')


class ReservistsViewSet(viewsets.ModelViewSet):
    queryset = Reservist.objects.prefetch_related('stages').all()
    serializer_class = ReservistsWebSerializer
