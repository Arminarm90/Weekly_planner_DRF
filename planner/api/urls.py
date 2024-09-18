from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # TasksGenericDetalView,
    # TasksGenericApiView,
    # DayGenericAPIView,
    # DayGenericDetailView,
    # WeekGenericAPIView,
    # WeekGenericDetailView,
    TaskAPIView,

)

# router = DefaultRouter()
# router.register(r"tasks", TaskVewsets)
# router.register(r"days", DayVewsets)
# router.register(r"weeks", WeekVewsets)

# urlpatterns = [
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path('tasks/', TaskAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskAPIView.as_view(), name='task-detail'),
    # path('days/', DayAPIView.as_view(), name='day-list'),
    # path('days/<int:pk>/', DayAPIView.as_view(), name='day-detail'),
    # path('weeks/', WeekAPIView.as_view(), name='week-list'),
    # path('weeks/<int:pk>/', WeekAPIView.as_view(), name='week-detail'),
]
