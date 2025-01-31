import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitnessApp.settings')
django.setup()

from workouts.models import Exercise


with open('exercise_data.json', 'r') as f:
    exercises = json.load(f)


for exercise in exercises:
    Exercise.objects.get_or_create(**exercise)

print("✅ Exercise database populated!")
