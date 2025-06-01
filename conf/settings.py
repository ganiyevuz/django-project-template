import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv.main import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, 'apps'))
load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ["true", "1", "t"]

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = []

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My apps

    # Third-party libraries
    'rest_framework',
    'drf_spectacular',
    'django_filters',
    'drf_standardized_errors',
    'corsheaders',
    'storages',
    'django_prometheus'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'conf.urls'
# AUTH_USER_MODEL = 'users.User'
APPEND_SLASH = False

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

WSGI_APPLICATION = 'conf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', default='postgres'),
        'PORT': os.getenv('DATABASE_PORT')
    },
    'POOL_OPTIONS': {
        'POOL_SIZE': 10,
        'MAX_OVERFLOW': 10,
        'RECYCLE': 24 * 60 * 60
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# S3 / MinIO Storage Settings
USE_S3_STORAGE = os.getenv('USE_S3_STORAGE', 'False').lower() in ['true', '1', 't']
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

if USE_S3_STORAGE:
    # S3 / MinIO Storage
    STORAGES = {
        "default": {
            "BACKEND": "shared.storage_backends.MediaMinIOStorage",
        },
        "staticfiles": {
            "BACKEND": "shared.storage_backends.StaticMinIOStorage",
        },
    }
    AWS_S3_USE_SSL = os.getenv('AWS_S3_USE_SSL', 'False').lower() in ['true', '1', 't']
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', None)
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', None)
    AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL', None)
    AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION', 's3v4')

    # Enable automatic file deletion when the corresponding object is deleted
    AWS_AUTO_CREATE_BUCKET = True
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    STATIC_URL = "static/"
    STATICFILES_LOCATION = 'static'
    MEDIA_FILES_LOCATION = 'media'
else:
    # Local Storage
    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    MEDIA_URL = "media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '10/minute',
    #     'user': '10/minute'
    # }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API',
    'DESCRIPTION': 'API for project',
    'VERSION': '1.0.0',
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATION_PARAMETERS": True,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]/[a-zA-Z0-9\-\_]+",
    # 'SCHEMA_PATH_PREFIX_TRIM': True,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'SECURITY': [{'Bearer': []}],
    "AUTHENTICATION": [
        {
            "name": "Session",
            "description": "Session-based authentication (for Django admin and browser-based sessions)",
            "schema": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Bearer token is required for JWT authentication. Admin panel uses session-based authentication.",
            },
        },
        {
            "name": "JWT",
            "description": "JWT-based authentication",
            "schema": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Use Bearer token for JWT authentication.",
            },
        },
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ALGORITHM': 'HS256',
    'UPDATE_LAST_LOGIN': True,
    # "TOKEN_OBTAIN_SERIALIZER": "apps.shared.rest_framework.CustomTokenObtainPairSerializer",

}
CACHES = {
    'default': {
        'BACKEND': 'django_prometheus.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('CACHE_BACKEND_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CACHE_OTP_TTL = 300
CACHE_OTP_KEY_PREFIX = 'otp'

SILENCED_SYSTEM_CHECKS = ['auth.E003']

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = os.getenv('TIME_ZONE')

LOGIN_URL = 'admin/'
LOGIN_REDIRECT_URL = '/'

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

if DEBUG:
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'SAMEORIGIN'

API_VERSION = os.getenv('BACKEND_VERSION', 'v1')
BACKEND_DOMAIN = os.getenv('BACKEND_DOMAIN', 'v1')
