from django.http import JsonResponse
from django.core.cache import cache
import time


class RateLimitingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        current_time = int(time.time())

        # تعداد درخواست‌های اخیر از آی‌پی مشخص
        key = f"rate_limit_{ip}_{current_time // 60}"  # محدودیت هر دقیقه
        request_count = cache.get(key, 0)

        if request_count >= 100:
            return JsonResponse({'error': 'Too many requests'}, status=429)

        cache.set(key, request_count + 1, timeout=60)  # افزایش شمارش درخواست
        response = self.get_response(request)
        return response
