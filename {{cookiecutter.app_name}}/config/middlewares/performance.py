import time
from django.utils.deprecation import MiddlewareMixin


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        print(f"Request to {request.path} took {duration:.2f} seconds")
        return response
