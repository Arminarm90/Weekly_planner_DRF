from .serialisers import TaskSerializer, DaySerializer, WeekSerializer
from ..models import Task, Day, Week
from rest_framework import viewsets


class TaskVewsets(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class DayVewsets(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class WeekVewsets(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
