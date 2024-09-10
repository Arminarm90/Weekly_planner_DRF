from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TasksGenericDetalView,
    TasksGenericApiView,
    DayGenericAPIView,
    DayGenericDetailView,
    WeekGenericAPIView,
    WeekGenericDetailView,
)

# router = DefaultRouter()
# router.register(r"tasks", TaskVewsets)
# router.register(r"days", DayVewsets)
# router.register(r"weeks", WeekVewsets)

# urlpatterns = [
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("tasks/", TasksGenericApiView.as_view(), name='tasks'),
    path("tasks/<pk>", TasksGenericDetalView.as_view(), name='tasks-detail'),
    path("day/", DayGenericAPIView.as_view(), name='day'),
    path("day/<pk>", DayGenericDetailView.as_view(), name='day-detail'),
    path("week/", WeekGenericAPIView.as_view(), name='week'),
    path("week/<pk>", WeekGenericDetailView.as_view(), name='week-detail'),
]
