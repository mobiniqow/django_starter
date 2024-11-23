from django.core.cache import cache
from django.http import JsonResponse


class CachingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cache_key = f"cache_{request.path}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response

        response = self.get_response(request)
        cache.set(cache_key, response, timeout=60 * 15)  # کش برای 15 دقیقه
        return response
