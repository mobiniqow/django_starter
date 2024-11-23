import logging


class LoggingMiddleware:
    """
    Middleware برای ثبت لاگ‌ها در هر درخواست.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # ثبت لاگ درخواست‌ها
        self.logger.info(f"Request received: {request.method} {request.path}")

        response = self.get_response(request)

        # ثبت لاگ پاسخ‌ها
        self.logger.info(f"Response status: {response.status_code}")

        return response