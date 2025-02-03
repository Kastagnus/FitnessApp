from rest_framework import serializers
from .models import FitnessGoal, FitnessGoalProgress

class FitnessGoalProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoalProgress
        fields = ["date", "progress_value"]

class FitnessGoalCreateSerializer(serializers.ModelSerializer):
    progress_entries = FitnessGoalProgressSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    starting_weight = serializers.FloatField(read_only=True)

    class Meta:
        model = FitnessGoal
        fields = [
            "id", "goal_type", "target_value", "starting_weight",
            "current_progress", "progress_percentage", "status", "progress_entries"
        ]

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()

class FitnessGoalUpdateSerializer(serializers.ModelSerializer):
    progress_entries = FitnessGoalProgressSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    starting_weight = serializers.FloatField(read_only=True)

    class Meta:
        model = FitnessGoal
        fields = [
            "id", "goal_type", "target_value", "starting_weight",
            "current_progress", "progress_percentage", "status", "progress_entries"
        ]
        #read only mode for updates
        extra_kwargs = {
            'goal_type': {'read_only': True}
        }

    def get_progress_percentage(self, obj):
        return obj.progress_percentage()
