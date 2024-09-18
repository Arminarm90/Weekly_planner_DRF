from rest_framework import serializers
from ..models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "duration_minutes",
            "audio_scripter_minutes",
            "copying_minutes",
            "dictation_minutes",
        ]  # Exclude 'user'

    def create(self, validated_data):
        # Get the user from the request context
        user = self.context["request"].user
        task = Task.objects.create(user=user, **validated_data)
        return task

    def to_representation(self, instance):
        # Get the original representation (default data for all fields)
        representation = super().to_representation(instance)

        # Remove any fields that have a value of 0 or None
        fields_to_remove = [
            "duration_minutes",
            "audio_scripter_minutes",
            "copying_minutes",
            "dictation_minutes",
        ]
        for field in fields_to_remove:
            if representation[field] == 0 or representation[field] is None:
                representation.pop(field)

        return representation


# class DaySerializer(serializers.ModelSerializer):
#     tasks = TaskSerializer(many=True, read_only=True)
#     # total_hours = serializers.SerializerMethodField()

#     class Meta:
#         model = Day
#         fields = "__all__"

#     # def get_total_hours(self, obj):
#     #     return obj.total_hours()


# class WeekSerializer(serializers.ModelSerializer):
#     days = DaySerializer(many=True, read_only=True)
#     # total_hours = serializers.SerializerMethodField()

#     class Meta:
#         model = Week
#         fields = "__all__"

    # def get_total_hours(self, obj):
    #     return obj.total_hours()
