from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError
import logging

logger = logging.getLogger(__name__)  # Logging for debugging if needed


def custom_exception_handler(exc, context):
    """Custom exception handler for cleaner API responses."""

    # Let DRF's default exception handler process the exception
    response = exception_handler(exc, context)

    # If response exists, modify it to return clean error messages
    if response is not None:
        custom_response = {"error": response.data}

        # Customize error messages for clarity
        if isinstance(exc, NotAuthenticated):
            custom_response["error"] = "Authentication credentials were not provided or are invalid."
        elif isinstance(exc, AuthenticationFailed):
            custom_response["error"] = "Invalid credentials. Please log in again."
        elif isinstance(exc, PermissionDenied):
            custom_response["error"] = "You do not have permission to perform this action."
        elif isinstance(exc, ObjectDoesNotExist):
            custom_response["error"] = "The requested resource was not found."
        elif isinstance(exc, ValidationError):
            custom_response["error"] = "Invalid data submitted."

        # Log the error (optional, useful for debugging)
        logger.error(f"API Exception: {exc} - Context: {context}")

        return Response(custom_response, status=response.status_code)

    # If the exception is not handled, return a generic error
    return Response(
        {"error": "An unexpected error occurred. Please try again later."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
