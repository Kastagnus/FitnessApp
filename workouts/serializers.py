from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise, Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.ReadOnlyField(source="exercise.name")

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'exercise_name', 'sets', 'reps', 'duration', 'distance']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'name', 'frequency', 'exercises', 'created_at']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        workout_plan = WorkoutPlan.objects.create(**validated_data)

        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout_plan=workout_plan, **exercise_data)

        return workout_plan

    def update(self, instance, validated_data):
        exercises_data = validated_data.pop('exercises', None)
        instance.name = validated_data.get('name', instance.name)
        instance.frequency = validated_data.get('frequency', instance.frequency)
        instance.save()

        if exercises_data is not None:
            instance.exercises.all().delete()  # Remove old exercises
            for exercise_data in exercises_data:
                WorkoutExercise.objects.create(workout_plan=instance, **exercise_data)

        return instance