# from django.urls import path
# from .views import FitnessGoalListCreateView, FitnessGoalDetailView
#
# urlpatterns = [
#     path('goals/', FitnessGoalListCreateView.as_view(), name='fitness-goal-list'),
#     path('goals/<int:pk>/', FitnessGoalDetailView.as_view(), name='fitness-goal-detail'),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FitnessGoalViewSet, FitnessGoalProgressViewSet

router = DefaultRouter()
router.register(r"goals", FitnessGoalViewSet, basename="fitness-goals")
router.register(r"progress", FitnessGoalProgressViewSet, basename="fitness-progress")

urlpatterns = [
    path("", include(router.urls)),
]

