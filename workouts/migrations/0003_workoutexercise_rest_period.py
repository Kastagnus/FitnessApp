# Generated by Django 5.1.5 on 2025-02-02 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_workoutplan_workoutexercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutexercise',
            name='rest_period',
            field=models.IntegerField(blank=True, help_text='Rest period in seconds between sets', null=True),
        ),
    ]
