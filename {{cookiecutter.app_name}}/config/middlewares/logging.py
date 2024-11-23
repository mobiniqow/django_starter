
from django.utils.deprecation import MiddlewareMixin

# ANSI codes for colors and styles
class LogColorMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # تنظیمات لاگ به صورت رنگی
        if response.status_code >= 400:
            log_color = '\033[91m'  # Red for errors (4xx, 5xx)
        elif response.status_code >= 300:
            log_color = '\033[93m'  # Yellow for redirects (3xx)
        else:
            log_color = '\033[92m'  # Green for successful responses (2xx)

        log_reset = '\033[0m'  # Reset color

        # ایجاد پیام لاگ برای ترمینال
        log_message = f"{log_color}Response: {response.status_code} {response.reason_phrase}{log_reset}"
        self.log_to_console(log_message)
        return response

    def log_to_console(self, message):
        # پرینت لاگ به همراه رنگ
        print(message)

# تنظیمات لاگ در settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'colored': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

