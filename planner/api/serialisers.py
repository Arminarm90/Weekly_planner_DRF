from rest_framework import serializers
from ..models import Task, Day, Week


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'duration_minutes']  # Exclude 'user'

    def create(self, validated_data):
        # Get the user from the request context
        user = self.context['request'].user
        task = Task.objects.create(user=user, **validated_data)
        return task
    
class DaySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    # total_hours = serializers.SerializerMethodField()

    class Meta:
        model = Day
        fields = "__all__"

    # def get_total_hours(self, obj):
    #     return obj.total_hours()


class WeekSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    # total_hours = serializers.SerializerMethodField()

    class Meta:
        model = Week
        fields = "__all__"

    # def get_total_hours(self, obj):
    #     return obj.total_hours()
