from rest_framework import serializers
from ..models import Task, Day, Week


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class DaySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    total_hours = serializers.SerializerMethodField()

    class Meta:
        model = Day
        fields = "__all__"

    def get_total_hours(self, obj):
        return obj.total_hours()


class WeekSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    total_hours = serializers.SerializerMethodField()

    class Meta:
        model = Week
        fields = "__all__"

    def get_total_hours(self, obj):
        return obj.total_hours()
