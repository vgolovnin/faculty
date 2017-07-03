from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


def index(request):
    return render(request, 'index.html')


class ReportsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportsSerializer
    queryset = Stage.objects.filter(stageset__templates__isnull=False).order_by('deadline')


@permission_classes([IsAuthenticated, ])
class ParticipationsViewSet(viewsets.ViewSet):
    def list(self, request):

        reservists_queryset = Reservist.objects.filter(category__isnull=False)\
            .select_related('category', 'status', 'department').all()
        particpations_queryset = Participation.objects.all()
        return Response({
            'reserve': ReservistsWebSerializer(reservists_queryset, many=True).data,
            'stages': StagesSerializer(Stage.objects.all(), many=True, context={'request': request}).data,
            'participations': ParticipationSerializer(particpations_queryset, many=True).data
        })

    def partial_update(self, request, pk=None):
        try:
            participation = Participation.objects.get(pk=pk)
        except Participation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ParticipationSerializer(participation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def reserveStatus(request, res_id):
    try:
        reservist = Reservist.objects.get(id=res_id)
    except Reservist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return render(request, 'status.html', context={'reservist': reservist})
