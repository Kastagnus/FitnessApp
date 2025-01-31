from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from .models import Exercise
from .serializers import ExerciseSerializer, WorkoutPlanSerializer
from rest_framework.permissions import IsAuthenticated
from .models import WorkoutPlan
from rest_framework.exceptions import NotAuthenticated
from drf_yasg import openapi

class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of predefined exercises.",
        responses={200: ExerciseSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WorkoutPlanListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all workout plans for the authenticated user.",
        responses={200: WorkoutPlanSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new workout plan with exercises.",
        responses={201: WorkoutPlanSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return WorkoutPlan.objects.none()
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("You must be logged in to view workout plans.")
        return WorkoutPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a workout plan by ID.",
        responses={200: WorkoutPlanSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a workout plan by ID.",
        responses={200: WorkoutPlanSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a workout plan by ID.",
        responses={200: WorkoutPlanSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a workout plan by ID.",
        responses={204: "Workout Plan Deleted"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return WorkoutPlan.objects.none()
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("You must be logged in to view workout plans.")
        return WorkoutPlan.objects.filter(user=self.request.user)