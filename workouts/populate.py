import os
import sys
import django
import json
"""
Docker container adapted script to populate database
"""
# Add the project directory to Python path
sys.path.append('/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitnessApp.settings')
django.setup()

from workouts.models import Exercise

with open('workouts/exercise_data.json', 'r') as f:
    exercises = json.load(f)

for exercise in exercises:
    Exercise.objects.get_or_create(**exercise)

print("Exercise database populated!")