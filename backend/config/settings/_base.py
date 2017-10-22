import json
import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_HOME = os.path.expanduser('~')
PROJECT_HOME = os.path.join(BASE_DIR, '../')

environ_path = os.path.join(BASE_DIR, '../.env.json')
with open(environ_path) as f:
    secrets = json.loads(f.read())


def get_secret(secret):
    try:
        return secrets[secret]
    except KeyError:
        raise ImproperlyConfigured('Required variable [{}] not configured'.format(secret))


def set_settings_module(module):
    if module in ['config.settings.development', 'config.settings.staging', 'config.settings.production', 'config.settings.celery_stage', 'config.settings.celery_prod']:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', module)
        print("Using configuration [{}]".format(module))
    else:
        raise ImproperlyConfigured('Wrong settings module for configuration')


set_settings_module(get_secret('django_settings_module'))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'collegesearch',
        'USER': 'dev',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
REACT_APP_DIR = os.path.join(BASE_DIR, '../../frontend')
STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'build', 'static')
]

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# Logging
LOG_PATH = os.path.join(BASE_DIR, '../../logs')
