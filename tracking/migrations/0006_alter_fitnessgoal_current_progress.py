# Generated by Django 5.1.5 on 2025-02-01 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_fitnessgoal_status_fitnessgoalprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessgoal',
            name='current_progress',
            field=models.FloatField(default=0.0, help_text='Current weight or lifting progress'),
        ),
    ]
