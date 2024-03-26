from core.settings.base import *
from datetime import timedelta
from decouple import config

DEBUG = True

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'USER': config('DB_USER'),
        'PASSWORD': config("DB_PASSWORD"),
        'NAME': config('DB_NAME'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/var/html/www/{{cookiecutter.app_name}}/template/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWED_HOSTS = ['*']

STATIC_URL = "/static/"

STATIC_ROOT = "/var/html/www/{{cookiecutter.app_name}}/static/"

MEDIA_URL = "/media/"

MEDIA_ROOT = "/var/html/www/{{cookiecutter.app_name}}/media/"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=45),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=99),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=99),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'auth': '7/min',
        'twenty_per_hour': '20/hour',
        'fifty_per_day': '50/day',
        # 'uploads': '20/day'
    },
}
