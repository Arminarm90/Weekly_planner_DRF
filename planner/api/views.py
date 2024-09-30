from .serialisers import TaskSerializer
from ..models import Task
from rest_framework import viewsets, permissions, generics
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions


class TaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=request.user.studentprofile)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        student = request.user.studentprofile
        data = request.data.copy()
        data['user'] = student.id  # Assign the student automatically
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save task with the authenticated user from context
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk, user=request.user.studentprofile)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk, user=request.user.studentprofile)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # class DayAPIView(APIView):
    #     permission_classes = [permissions.IsAuthenticated]

    #     def get(self, request, *args, **kwargs):
    #         days = Day.objects.filter(user=request.user)
    #         data = []

    #         for day in days:
    #             tasks = Task.objects.filter(user=request.user, day=day)
    #             task_data = TaskSerializer(tasks, many=True).data

    #             total_minutes = sum(
    #                 [
    #                     task.duration_minutes
    #                     + task.audio_scripter_minutes
    #                     + task.copying_minutes
    #                     + task.dictation_minutes
    #                     for task in tasks
    #                 ]
    #             )
    #             total_hours = total_minutes / 60

    #             day_data = {
    #                 "id": day.id,
    #                 "date": day.date,
    #                 "total_hours": total_hours,
    #                 "AnkiDroid/Ankiapp": day.AnkiDroid_Ankiapp,
    #                 "word_count": day.word_count,
    #                 "tasks": task_data,
    #             }
    #             data.append(day_data)

    #         return Response(data)

    #     def post(self, request, *args, **kwargs):
    #         serializer = DaySerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(user=request.user)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     def put(self, request, pk, *args, **kwargs):
    #         day = get_object_or_404(Day, pk=pk, user=request.user)
    #         serializer = DaySerializer(day, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     def delete(self, request, pk, *args, **kwargs):
    #         day = get_object_or_404(Day, pk=pk, user=request.user)
    #         day.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    # class WeekAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     weeks = Week.objects.filter(user=request.user)
    #     data = []

    #     for week in weeks:
    #         # Get all days in this week
    #         days = Day.objects.filter(
    #             user=request.user, date__gte=week.start_date, date__lte=week.end_date
    #         )

    #         tasks = Task.objects.filter(
    #             user=request.user,
    #             day__date__gte=week.start_date,
    #             day__date__lte=week.end_date,
    #         )
    #         task_data = TaskSerializer(tasks, many=True).data

    #         total_minutes = sum(
    #             [
    #                 task.duration_minutes
    #                 + task.audio_scripter_minutes
    #                 + task.copying_minutes
    #                 + task.dictation_minutes
    #                 for task in tasks
    #             ]
    #         )
    #         total_hours = total_minutes / 60

    #         total_Anki_words = (
    #             days.aggregate(Sum("AnkiDroid_Ankiapp"))["AnkiDroid_Ankiapp__sum"] or 0
    #         )
    #         total_words_count = (
    #             days.aggregate(Sum("word_count"))["word_count__sum"] or 0
    #         )

    #         # total_minutes = (
    #         #     tasks.aggregate(Sum("duration_minutes"))["duration_minutes__sum"] or 0
    #         # )
    #         # total_hours = total_minutes / 60

    #         week_data = {
    #             "id": week.id,
    #             "start_date": week.start_date,
    #             "end_date": week.end_date,
    #             "total_hours": total_hours,
    #             "AnkiDroid/Ankiapp": total_Anki_words,
    #             "word_count": total_words_count,
    #             # "tasks": task_data,
    #         }
    #         data.append(week_data)

    #     return Response(data)

    # def post(self, request, *args, **kwargs):
    #     serializer = WeekSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, *args, **kwargs):
    #     week = get_object_or_404(Week, pk=pk, user=request.user)
    #     serializer = WeekSerializer(week, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, *args, **kwargs):
    #     week = get_object_or_404(Week, pk=pk, user=request.user)
    #     week.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class TasksGenericApiView(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # Ensure only the authenticated user sees their tasks
#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)

#     # Automatically associate the task with the logged-in user
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class TasksGenericDetalView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # Ensure only the authenticated user sees their tasks
#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)


# class DayGenericAPIView(generics.ListCreateAPIView):
#     queryset = Day.objects.all()
#     serializer_class = DaySerializer

#     # Ensure only the authenticated user sees their tasks
#     def get_queryset(self):
#         return Day.objects.filter(user=self.request.user)

#     # Override the list method to add total hours for each day
#     def list(self, request, *args, **kwargs):
#         days = self.get_queryset()
#         data = []

#         for day in days:
#             # Get tasks for this day
#             tasks = Task.objects.filter(user=self.request.user, day=day)
#             task_data = TaskSerializer(tasks, many=True).data

#             # Calculate total minutes and convert to hours
#             total_minutes = tasks.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
#             total_hours = total_minutes / 60

#             day_data = {
#                 'id': day.id,
#                 'date': day.date,
#                 'total_hours': total_hours,
#                 'tasks': task_data
#             }
#             data.append(day_data)

#         return Response(data)

# class DayGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Day.objects.all()
#     serializer_class = DaySerializer

#     # Ensure only the authenticated user sees their tasks
#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)


# class WeekGenericAPIView(generics.ListCreateAPIView):
#     queryset = Week.objects.all()
#     serializer_class = WeekSerializer

#     # Ensure only the authenticated user sees their tasks
#     def get_queryset(self):
#         return Week.objects.filter(user=self.request.user)

#     # Override the list method to add total hours for each week
#     def list(self, request, *args, **kwargs):
#         weeks = self.get_queryset()
#         data = []

#         for week in weeks:
#             # Get tasks for the entire week
#             tasks = Task.objects.filter(
#                 user=self.request.user,
#                 day__date__gte=week.start_date,
#                 day__date__lte=week.end_date
#             )
#             task_data = TaskSerializer(tasks, many=True).data

#             # Calculate total minutes and convert to hours
#             total_minutes = tasks.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
#             total_hours = total_minutes / 60

#             week_data = {
#                 'id': week.id,
#                 'start_date': week.start_date,
#                 'end_date': week.end_date,
#                 'total_hours': total_hours,
#                 'tasks': task_data
#             }
#             data.append(week_data)

#         return Response(data)


# class WeekGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Week.objects.all()
#     serializer_class = WeekSerializer

#     # Ensure only the authenticated user sees their tasks
#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)
