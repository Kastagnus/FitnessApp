from rest_framework import serializers
from .models import FitnessGoal, FitnessGoalProgress

class FitnessGoalProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoalProgress
        fields = ["date", "progress_value"]

class FitnessGoalSerializer(serializers.ModelSerializer):
    progress_entries = FitnessGoalProgressSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    starting_weight = serializers.FloatField(read_only=True)  # ✅ Make starting weight read-only
    goal_type = serializers.CharField(source="get_goal_type_display", read_only=True)
    class Meta:
        model = FitnessGoal
        fields = [
            "id", "goal_type", "target_value", "starting_weight",
            "current_progress", "progress_percentage", "status", "progress_entries"
        ]

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()  # ✅ Call model method

    def get_progress_entries(self, obj):
        """Retrieve all progress entries sorted by date."""
        return FitnessGoalProgressSerializer(obj.progress_entries.order_by("date"), many=True).data



