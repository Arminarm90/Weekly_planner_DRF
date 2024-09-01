from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskVewsets, DayVewsets, WeekVewsets

router = DefaultRouter()
router.register(r"tasks", TaskVewsets)
router.register(r"days", DayVewsets)
router.register(r"weeks", WeekVewsets)

urlpatterns = [
    path("", include(router.urls)),
]
