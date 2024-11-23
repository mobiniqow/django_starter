from rest_framework.response import Response
from rest_framework import status

class ApiResponse:
    def __init__(self, status_code=status.HTTP_200_OK, status_text="success", message="", data=None, error_code=None, errors=None):
        self.status_code = status_code
        self.status_text = status_text
        self.message = message
        self.data = data if data else {}
        self.error_code = error_code
        self.errors = errors if errors else []

    def success(self, message="", data=None):
        """Generate a success response"""
        return Response({
            "status": "success",
            "message": message or self.message,
            "data": data or self.data
        }, status=self.status_code)

    def error(self, message="", error_code=None, errors=None):
        """Generate an error response"""
        return Response({
            "status": "error",
            "message": message or self.message,
            "error_code": error_code or self.error_code,
            "errors": errors or self.errors
        }, status=self.status_code)

    def warning(self, message="", data=None):
        """Generate a warning response"""
        return Response({
            "status": "warning",
            "message": message or self.message,
            "data": data or self.data
        }, status=self.status_code)

    @staticmethod
    def format_errors(errors):
        """Helper method to format errors"""
        return [{"field": error.get("field"), "message": error.get("message")} for error in errors]
