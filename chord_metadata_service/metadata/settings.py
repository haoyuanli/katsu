"""
Django settings for metadata project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import logging

from urllib.parse import quote, urlparse
from dotenv import load_dotenv

from .. import __version__

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SERVICE_SECRET_KEY", '=p1@hhp5m4v0$c#eba3a+rx!$9-xk^q*7cb9(cd!wn1&_*osyc')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("CHORD_DEBUG", "true").lower() == "true"


# CHORD-specific settings

CHORD_URL = os.environ.get("CHORD_URL")  # Leave None if not specified, for running in other contexts

# SECURITY WARNING: Don't run with CHORD_PERMISSIONS turned off in production,
# unless an alternative permissions system is in place.
CHORD_PERMISSIONS = os.environ.get("CHORD_PERMISSIONS", str(not DEBUG)).lower() == "true"

CHORD_SERVICE_ARTIFACT = "metadata"
CHORD_SERVICE_TYPE_NO_VER = f"ca.c3g.chord:{CHORD_SERVICE_ARTIFACT}"
CHORD_SERVICE_TYPE = f"{CHORD_SERVICE_TYPE_NO_VER}:{__version__}"
CHORD_SERVICE_ID = os.environ.get("SERVICE_ID", CHORD_SERVICE_TYPE_NO_VER)

# SECURITY WARNING: don't run with AUTH_OVERRIDE turned on in production!
AUTH_OVERRIDE = not CHORD_PERMISSIONS


# Allowed hosts - TODO: Derive from CHORD_URL

CHORD_HOST = urlparse(CHORD_URL or "").netloc
ALLOWED_HOSTS = [CHORD_HOST or "localhost"]
if DEBUG:
    ALLOWED_HOSTS = list(set(ALLOWED_HOSTS + ["localhost", "127.0.0.1", "[::1]"]))

APPEND_SLASH = False

# Bento misc. settings

SERVICE_TEMP = os.environ.get("SERVICE_TEMP")

#  - DRS URL - by default in Bento Singularity context, use internal NGINX DRS (to avoid auth hassles)
NGINX_INTERNAL_SOCKET = quote(os.environ.get("NGINX_INTERNAL_SOCKET", "/chord/tmp/nginx_internal.sock"), safe="")
DRS_URL = os.environ.get("DRS_URL", f"http+unix://{NGINX_INTERNAL_SOCKET}/api/drs").strip().rstrip("/")

# Candig-specific settings

CANDIG_AUTHORIZATION = os.environ.get("CANDIG_AUTHORIZATION")
CANDIG_OPA_URL = os.environ.get("CANDIG_OPA_URL")
CANDIG_OPA_SECRET = os.getenv("CANDIG_OPA_SECRET", "my-secret-beacon-token")

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'chord_metadata_service.chord.apps.ChordConfig',
    'chord_metadata_service.experiments.apps.ExperimentsConfig',
    'chord_metadata_service.patients.apps.PatientsConfig',
    'chord_metadata_service.phenopackets.apps.PhenopacketsConfig',
    'chord_metadata_service.mcode.apps.McodeConfig',
    'chord_metadata_service.resources.apps.ResourcesConfig',
    'chord_metadata_service.restapi.apps.RestapiConfig',

    'corsheaders',
    'django_filters',
    'rest_framework',
    'django_nose',
    'rest_framework_swagger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'bento_lib.auth.django_remote_user.BentoRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chord_metadata_service.restapi.datasets_authz_middleware.DatasetsAuthzMiddleware',
]

CORS_ALLOWED_ORIGINS = []

ROOT_URLCONF = 'chord_metadata_service.metadata.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'chord_metadata_service.metadata.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}

# if we are running the test suite, only log CRITICAL messages
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    logging.disable(logging.CRITICAL)


# function to read postgres password file
def get_secret(path):
    try:
        with open(path) as f:
            return f.readline().strip()
    except BaseException as err:
        print(f"Unexpected {err}, {type(err)}")
        raise


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DATABASE", 'metadata'),
        'USER': os.environ.get("POSTGRES_USER", 'admin'),
        'PASSWORD': get_secret(
            os.environ["POSTGRES_PASSWORD_FILE"]
        ) if "POSTGRES_PASSWORD_FILE" in os.environ else os.environ.get("POSTGRES_PASSWORD", "admin"),

        # Use sockets if we're inside a CHORD container / as a priority
        'HOST': os.environ.get("POSTGRES_SOCKET_DIR", os.environ.get("POSTGRES_HOST", "localhost")),
        'PORT': os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# Django default cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

FHIR_INDEX_NAME = 'fhir_metadata'

# Set to True to run ES for FHIR index
ELASTICSEARCH = False

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'bento_lib.auth.django_remote_user.BentoRemoteUserAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': (
        # allows serializers to use snake_case field names, but parse incoming data as camelCase
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': ['chord_metadata_service.chord.permissions.OverrideOrSuperUserOnly'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = ["bento_lib.auth.django_remote_user.BentoRemoteUserBackend"] + (
    ["django.contrib.auth.backends.ModelBackend"] if DEBUG else [])


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Cache time constant
CACHE_TIME = int(os.getenv("CACHE_TIME", 60 * 60 * 2))
