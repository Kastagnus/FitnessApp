from django.urls import path
from .views import (
    WorkoutSessionListCreateView,
    WorkoutSessionDetailView,
    ExerciseSetProgressUpdateView
)

urlpatterns = [
    path('workout-sessions/', WorkoutSessionListCreateView.as_view(), name='workout-session-list'),
    path('workout-sessions/<int:pk>/', WorkoutSessionDetailView.as_view(), name='workout-session-detail'),
    path('sessions/<int:session_id>/exercises/<int:exercise_id>/sets/<int:set_number>/',
         ExerciseSetProgressUpdateView.as_view(),
         name='set-progress-update'),
]