from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import FitnessGoal, FitnessGoalProgress
from .serializers import FitnessGoalProgressSerializer, FitnessGoalUpdateSerializer, \
    FitnessGoalCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status


class FitnessGoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return FitnessGoalUpdateSerializer
        return FitnessGoalCreateSerializer

    def get_queryset(self):
        """Return fitness goals for the authenticated user."""
        if getattr(self, 'swagger_fake_view', False):
            return FitnessGoal.objects.none()
        return FitnessGoal.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Displaying all fitness goals for the authenticated user.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a fitness goal by its ID for the authenticated user.
        """
        goal = self.get_object()
        if goal.user != request.user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
        
    def perform_create(self, serializer):
        """
        Assigns the authenticated user and saves initial progress.
        Pauses any existing active goals before creating a new one.
        """
        user = self.request.user
        current_progress = self.request.data.get("current_progress", 0.0)

        # Pause any active goals before creating a new one
        FitnessGoal.objects.filter(user=user, status="active").update(status="paused")

        # Create the new fitness goal
        goal = serializer.save(user=user, current_progress=current_progress, status="active")

        # Automatically create an initial progress entry
        FitnessGoalProgress.objects.create(goal=goal, progress_value=current_progress)

    def perform_update(self, serializer):
        """
        Tracks progress history when updating current progress.
        Updates the fitness goal and logs the progress.
        """
        goal = self.get_object()
        new_progress = self.request.data.get("current_progress", goal.current_progress)
        status = goal.status
        if goal.goal_type == "lose_weight":
            if new_progress <= goal.target_value:
                status = "completed"
        elif goal.goal_type == "gain_muscle":
            if new_progress >= goal.target_value:
                status = "completed"
        # Save the updated goal progress
        serializer.save(current_progress=new_progress, status=status)

        # Log progress history
        FitnessGoalProgress.objects.create(goal=goal, progress_value=new_progress)

    @swagger_auto_schema(
        operation_description="Create a new fitness goal (Lose Weight / Gain Muscle).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "goal_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["lose_weight", "gain_muscle"],
                    description="Choose between 'lose_weight' or 'gain_muscle'."
                ),
                "target_value": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format=openapi.FORMAT_FLOAT,
                    description="Target weight (kg) for weight loss or strength goal (kg) for muscle gain."
                ),
                "current_progress": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format=openapi.FORMAT_FLOAT,
                    description="Current weight progress."
                ),
            },
            required=["goal_type", "target_value", "current_progress"],
        ),
        responses={201: FitnessGoalCreateSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing fitness goal.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'target_value': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format=openapi.FORMAT_FLOAT,
                    description="Target weight (kg) for weight loss or strength goal (kg) for muscle gain."
                ),
                "current_progress": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format=openapi.FORMAT_FLOAT,
                    description="Update user's current weight or lifting progress."
                ),
            },
            required=["current_progress"],
        ),
        responses={200: FitnessGoalUpdateSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the status of a fitness goal (active, paused, completed, cancelled).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["active", "paused", "completed", "cancelled"],
                    description="Set the status of the goal."
                ),
            },
            required=["status"],
        ),
        responses={200: "Goal status updated"},
    )
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        """Allows users to update their goal status (pause, complete, cancel)."""
        goal = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["active", "paused", "completed", "cancelled"]:
            return Response({"error": "Invalid status."}, status=400)

        goal.status = new_status
        goal.save()
        return Response({"message": f"Goal status updated to {new_status}."})


class FitnessGoalProgressViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for retrieving progress history of all the goals."""
    serializer_class = FitnessGoalProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return FitnessGoalProgress.objects.none()
        return FitnessGoalProgress.objects.filter(goal__user=self.request.user)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve progress history for a specific fitness goal.",
        responses={200: FitnessGoalProgressSerializer(many=True)},
    )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve all progress entries for a specific fitness goal.
        """
        fitnessgoal_id = kwargs.get('pk')
        progress_entries = self.get_queryset().filter(goal_id=fitnessgoal_id)

        if not progress_entries.exists():
            return Response(
                {"detail": "No progress entries found for this fitness goal."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(progress_entries, many=True)
        return Response(serializer.data)