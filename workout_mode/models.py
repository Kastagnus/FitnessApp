from django.contrib.auth.models import User
from django.db import models
from workouts.models import WorkoutExercise, WorkoutPlan


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
            ('PAUSED', 'Paused')
        ],
        default='IN_PROGRESS'
    )

class SessionExercise(models.Model):
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercises_progress')
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('SKIPPED', 'Skipped')
        ],
        default='PENDING'
    )

class ExerciseSetProgress(models.Model):
    session_exercise = models.ForeignKey(SessionExercise, on_delete=models.CASCADE, related_name='sets_progress')
    set_number = models.IntegerField()
    completed = models.BooleanField(default=False)
    actual_reps = models.IntegerField(null=True, blank=True)
    actual_duration = models.IntegerField(null=True, blank=True)
    actual_distance = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
