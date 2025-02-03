from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class FitnessGoal(models.Model):
    GOAL_CHOICES = [
        ("lose_weight", "Lose Weight"),
        ("gain_muscle", "Gain Muscle"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fitness_goals")
    goal_type = models.CharField(max_length=20, choices=GOAL_CHOICES)
    target_value = models.FloatField(help_text="Target weight (kg) or lifting goal (kg)")
    starting_weight = models.FloatField(help_text="Starting weight (kg) or lifting progress (kg)")
    current_progress = models.FloatField(help_text="Current weight or lifting progress", default=0.0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("paused", "Paused"), ("completed", "Completed"), ("cancelled", "Cancelled")],
        default="active"
    )
    def progress_percentage(self):
        """Calculate progress based on goal type."""
        if self.goal_type == "lose_weight":
            if self.current_progress > self.target_value:  # Ensure valid range
                return round(
                    ((self.starting_weight - self.current_progress) / (self.starting_weight - self.target_value)) * 100,
                    2)
        elif self.goal_type == "gain_muscle":
            return round(((self.current_progress - self.starting_weight) / (self.target_value - self.starting_weight)) * 100, 2)

        return 0.0  # Default Value

    def save(self, *args, **kwargs):
        if not self.starting_weight:
            self.starting_weight = self.current_progress  # Set starting weight
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()} ({self.progress_percentage()}%)"

class FitnessGoalProgress(models.Model):
    goal = models.ForeignKey(FitnessGoal, on_delete=models.CASCADE, related_name="progress_entries")
    date = models.DateTimeField(default=now)
    progress_value = models.FloatField(help_text="User's progress at this point in time")

    def __str__(self):
        return f"{self.goal.user.username} - {self.goal.goal_type} - {self.progress_value}kg on {self.date.strftime('%Y-%m-%d')}, target to reach - {self.goal.target_value}kg"


