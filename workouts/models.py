from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    target_muscles = models.CharField(max_length=255)
    instructions = models.TextField()

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_plans")
    name = models.CharField(max_length=255)
    frequency = models.CharField(max_length=100, help_text="e.g., 3 times per week")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey("workouts.Exercise", on_delete=models.CASCADE)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(null=True, blank=True, help_text="Reps per set")
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    distance = models.FloatField(null=True, blank=True, help_text="Distance in meters (for cardio exercises)")
    rest_period = models.IntegerField(null=True, blank=True, help_text="Rest period in seconds between sets")  # Added this

    def __str__(self):
        return f"{self.exercise.name} - {self.workout_plan.name}"