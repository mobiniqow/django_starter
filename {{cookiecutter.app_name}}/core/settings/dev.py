from datetime import timedelta
from core.settings.base import *
from decouple import RepositoryEnv
import os

# env_config = RepositoryEnv(os.path.join(BASE_DIR, 'azmon/settings/.env.dev'))
# env_config = env_config.data
DEBUG = True
INSTALLED_APPS.append("debug_toolbar")
INSTALLED_APPS.append("django_extensions")
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings.dev"
ALLOWED_HOSTS = ["*"]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'world',
#         'USER': 'mobiniqow',
#         'PASSWORD': 'docker',
#         'HOST': 'db',
#         'PORT': 5432
#     }
# }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS  = [os.path.join(BASE_DIR, "static")]
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
# debug toolbar config
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
# show in drf
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
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
