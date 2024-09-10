from .serialisers import TaskSerializer, DaySerializer, WeekSerializer
from ..models import Task, Day, Week
from rest_framework import viewsets, permissions, generics
from django.db.models import Sum
from rest_framework.response import Response


class TasksGenericApiView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure only the authenticated user sees their tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # Automatically associate the task with the logged-in user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TasksGenericDetalView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure only the authenticated user sees their tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class DayGenericAPIView(generics.ListCreateAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    # Ensure only the authenticated user sees their tasks
    def get_queryset(self):
        return Day.objects.filter(user=self.request.user)

    # Override the list method to add total hours for each day
    def list(self, request, *args, **kwargs):
        days = self.get_queryset()
        data = []

        for day in days:
            # Get tasks for this day
            tasks = Task.objects.filter(user=self.request.user, day=day)
            task_data = TaskSerializer(tasks, many=True).data

            # Calculate total minutes and convert to hours
            total_minutes = tasks.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
            total_hours = total_minutes / 60

            day_data = {
                'id': day.id,
                'date': day.date,
                'total_hours': total_hours,
                'tasks': task_data
            }
            data.append(day_data)

        return Response(data)

class DayGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    # Ensure only the authenticated user sees their tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class WeekGenericAPIView(generics.ListCreateAPIView):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

    # Ensure only the authenticated user sees their tasks
    def get_queryset(self):
        return Week.objects.filter(user=self.request.user)

    # Override the list method to add total hours for each week
    def list(self, request, *args, **kwargs):
        weeks = self.get_queryset()
        data = []

        for week in weeks:
            # Get tasks for the entire week
            tasks = Task.objects.filter(
                user=self.request.user, 
                day__date__gte=week.start_date, 
                day__date__lte=week.end_date
            )
            task_data = TaskSerializer(tasks, many=True).data

            # Calculate total minutes and convert to hours
            total_minutes = tasks.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
            total_hours = total_minutes / 60

            week_data = {
                'id': week.id,
                'start_date': week.start_date,
                'end_date': week.end_date,
                'total_hours': total_hours,
                'tasks': task_data
            }
            data.append(week_data)

        return Response(data)


class WeekGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

    # Ensure only the authenticated user sees their tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
