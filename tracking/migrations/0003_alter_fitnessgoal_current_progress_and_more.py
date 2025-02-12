# Generated by Django 5.1.5 on 2025-02-01 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_remove_fitnessgoal_starting_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessgoal',
            name='current_progress',
            field=models.FloatField(help_text='Current weight or lifting progress'),
        ),
        migrations.AlterField(
            model_name='fitnessgoal',
            name='target_value',
            field=models.FloatField(help_text='Target weight (kg) or lifting goal (kg)'),
        ),
    ]
