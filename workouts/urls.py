from django.urls import path
from .views import ExerciseListView, WorkoutPlanListCreateView, WorkoutPlanDetailView

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('workout-plans/', WorkoutPlanListCreateView.as_view(), name='workout-plan-list-create'),
    path('workout-plans/<int:pk>/', WorkoutPlanDetailView.as_view(), name='workout-plan-detail'),

]
