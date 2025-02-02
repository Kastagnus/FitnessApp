from django.http import Http404
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from .models import WorkoutSession, SessionExercise, ExerciseSetProgress
from .serializers import WorkoutSessionSerializer, SessionExerciseSerializer, ExerciseSetProgressSerializer
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all workout sessions for the authenticated user.",
        responses={
            200: WorkoutSessionSerializer(many=True),
            401: "Not authenticated"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Start a new workout session with selected workout plan.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['workout_plan'],
            properties={
                'workout_plan': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the workout plan to use"
                )
            }
        ),
        responses={
            201: WorkoutSessionSerializer,
            400: "Invalid workout plan ID",
            401: "Not authenticated"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        return WorkoutSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        #Pause any active sessions when new session is created
        WorkoutSession.objects.filter(
            user=self.request.user,
            status='IN_PROGRESS'
        ).update(status='PAUSED')
        serializer.save(user=self.request.user)

class WorkoutSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific workout session.",
        responses={
            200: WorkoutSessionSerializer,
            404: "Session not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update workout session status (complete/cancel).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['COMPLETED', 'CANCELLED'],
                    description="New status of the session"
                )
            }
        ),
        responses={
            200: WorkoutSessionSerializer,
            400: "Invalid status",
            404: "Session not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a workout session.",
        responses={
            204: "Workout Session successfully deleted",
            404: "Session not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        return WorkoutSession.objects.filter(user=self.request.user)

class ExerciseSetProgressUpdateView(generics.UpdateAPIView):
    serializer_class = ExerciseSetProgressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update progress for a specific exercise set.",
        manual_parameters=[
            openapi.Parameter('session_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
            openapi.Parameter('exercise_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
            openapi.Parameter('set_number', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        ],
        request_body=ExerciseSetProgressSerializer
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        session_id = self.kwargs.get('session_id')
        exercise_id = self.kwargs.get('exercise_id')
        set_number = self.kwargs.get('set_number')

        try:
            return ExerciseSetProgress.objects.get(
                session_exercise__workout_session_id=session_id,
                session_exercise__workout_exercise_id=exercise_id,
                set_number=set_number
            )
        except ExerciseSetProgress.DoesNotExist:
            raise Http404("Set progress not found")
    # def patch(self, request, session_id, exercise_id, set_number):
    #     try:
    #         set_progress = ExerciseSetProgress.objects.get(
    #             session_exercise__workout_session_id=session_id,
    #             session_exercise__workout_exercise_id=exercise_id,
    #             set_number=set_number
    #         )
    #         serializer = self.get_serializer(set_progress, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         return Response(serializer.data)
    #     except ExerciseSetProgress.DoesNotExist:
    #         return Response({"error": "Set not found"}, status=404)