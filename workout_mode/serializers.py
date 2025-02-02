from rest_framework import serializers
from .models import WorkoutSession, SessionExercise, ExerciseSetProgress
from workouts.serializers import WorkoutPlanSerializer


class ExerciseSetProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSetProgress
        fields = ['set_number', 'completed', 'actual_reps', 'actual_duration',
                  'actual_distance', 'notes']

    def update(self, instance, validated_data):
        # Update the set progress
        instance = super().update(instance, validated_data)

        # Get the session exercise
        session_exercise = instance.session_exercise

        # Get all sets for this exercise
        all_sets = session_exercise.sets_progress.all()
        completed_sets = all_sets.filter(completed=True).count()
        total_sets = all_sets.count()

        # Update session exercise status based on sets completion
        if completed_sets == total_sets:
            session_exercise.status = 'COMPLETED'
        elif completed_sets > 0:
            session_exercise.status = 'IN_PROGRESS'
        else:
            session_exercise.status = 'PENDING'

        session_exercise.save()

        return instance

class SessionExerciseSerializer(serializers.ModelSerializer):
    sets_progress = ExerciseSetProgressSerializer(many=True, read_only=True)
    exercise_name = serializers.ReadOnlyField(source='workout_exercise.exercise.name')
    planned = serializers.SerializerMethodField()

    class Meta:
        model = SessionExercise
        fields = ['workout_exercise', 'exercise_name', 'status', 'planned',
                  'sets_progress']

    def get_planned(self, obj):
        return {
            'sets': obj.workout_exercise.sets,
            'reps': obj.workout_exercise.reps,
            'duration': obj.workout_exercise.duration,
            'distance': obj.workout_exercise.distance,
            'rest_period': obj.workout_exercise.rest_period
        }


class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises_progress = SessionExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = ['id', 'workout_plan', 'status', 'started_at', 'ended_at',
                  'exercises_progress']

    def create(self, validated_data):
        workout_session = WorkoutSession.objects.create(**validated_data)
        workout_plan = validated_data['workout_plan']

        # Create SessionExercise for each exercise in the workout plan
        for workout_exercise in workout_plan.exercises.all():
            session_exercise = SessionExercise.objects.create(
                workout_session=workout_session,
                workout_exercise=workout_exercise
            )

            # Create ExerciseSetProgress for each set
            for set_number in range(1, workout_exercise.sets + 1):
                ExerciseSetProgress.objects.create(
                    session_exercise=session_exercise,
                    set_number=set_number
                )

        return workout_session