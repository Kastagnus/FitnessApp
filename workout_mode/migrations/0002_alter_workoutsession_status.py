# Generated by Django 5.1.5 on 2025-02-02 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_mode', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutsession',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('PAUSED', 'Paused')], default='IN_PROGRESS', max_length=20),
        ),
    ]
