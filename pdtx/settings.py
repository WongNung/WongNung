"""
Django settings for pdtx project.

Generated by 'django-admin startproject' using Django 4.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import json
from pathlib import Path
from datetime import timedelta
import re

import tmdbsimple as tmdb
from decouple import Csv, config

from . import typings

TMDB_API_KEY = config("TMDB_API_KEY")
tmdb.API_KEY = TMDB_API_KEY
tmdb.REQUESTS_TIMEOUT = (2, 5)

typings.setup()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
OAUTH_FILE = "oauth_credentials.json"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="your_secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=Csv(), default="127.0.0.1,localhost"
)

PGCRYPTO_KEY = config("PGCRYPTO_KEY", default="your_pgcrypto_key")

# Application definition
INSTALLED_APPS = [
    "wongnung.apps.WongnungConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.discord",
    'allauth.mfa',
    "axes",
    "tailwind",
    "theme",
    "django_htmx",
    'pgcrypto',
]

if DEBUG:
    INSTALLED_APPS += [
        "django_browser_reload",
    ]

# Tailwind configuration
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = ["127.0.0.1"]

# NPM executable for Tailwind
NPM_BIN_PATH = config("NPM_BIN_PATH", default="")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "wongnung.middlewares.LocalTimeMiddleware",
    "wongnung.middlewares.EnsureUserProfileMiddleware",
    "axes.middleware.AxesMiddleware",
    'wongnung.middlewares.AdminOnlyMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = "pdtx.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pdtx.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME", default="wongnung"),
        "USER": config("DATABASE_USERNAME", default="wongnung"),
        "PASSWORD": config("DATABASE_PASSWORD", default="password"),
        "HOST": config("DATABASE_HOST", default="localhost"),
        "PORT": config("DATABASE_PORT", default="5432"),
    }
}

# AXES configuration
AXES_HANDLER = "axes.handlers.cache.AxesCacheHandler"

AXES_FAILURE_LIMIT = 9
AXES_COOLOFF_TIME = timedelta(minutes=10)

# Caching
CACHES = {
    "default": {
        "BACKEND": "pdtx.UnsafeKeyDatabaseCache",
        "LOCATION": "wongnung_cache",
    },
    "searches": {
        "BACKEND": "pdtx.UnsafeKeyDatabaseCache",
        "LOCATION": "wongnung_search_cache",
    },
    "axes": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": f'{config("MEMCACHED_HOST", default="localhost")}:{config("MEMCACHED_PORT", default="11211")}'
    }
}

AXES_CACHE = "axes"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = config("APP_TZ", default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"

# User-uploaded media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Email backend & settings
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.example.com")
EMAIL_PORT = config("EMAIL_PORT", default="587")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="wongnung@example.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="password")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

if EMAIL_BACKEND == "django.core.mail.backends.filebased.EmailBackend":
    EMAIL_FILE_PATH = BASE_DIR / str(config("FILEBASED_EMAIL_PATH", default="test-mails"))

SITE_ID = 4
LOGIN_REDIRECT_URL = "/"
ACCOUNT_UNIQUE_EMAIL = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "github": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "discord": {
        "SCOPE": [
            "email",
            "identify",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}

if os.path.exists(BASE_DIR / OAUTH_FILE):
    with open(BASE_DIR / OAUTH_FILE) as oauth_file:
        CREDENTIALS = json.load(oauth_file)

    for auth_provider in tuple(CREDENTIALS.keys()):
        if any(
            (
                not CREDENTIALS[auth_provider],
                not CREDENTIALS[auth_provider]["client_id"],
                not CREDENTIALS[auth_provider]["secret"],
            )
        ):
            continue
        SOCIALACCOUNT_PROVIDERS[auth_provider].update(
            {
                "APP": {
                    "client_id": CREDENTIALS[auth_provider]["client_id"],
                    "secret": CREDENTIALS[auth_provider]["secret"],
                },
            }
        )

SOCIALACCOUNT_ADAPTER = "wongnung.adapter.CancellableAccountAdapter"

if not DEBUG and config("HTTPS", cast=bool, default=False):
    CSRF_TRUSTED_ORIGINS = [f"https://{address}" for address in ALLOWED_HOSTS]
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            "formatter": "app",
        },
    },
    "loggers": {
        'django.server': {
            'filters': ['skip_static_and_homepage_requests'],
        },
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
    'filters': {
        'skip_static_and_homepage_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: not re.match(r'.*GET /static/.*|.*GET / HTTP/.*', record.getMessage()),
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

AUTH_USER_MODEL = 'wongnung.CustomUser'