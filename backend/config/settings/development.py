from config.settings._base import *

LOG_PATH = os.path.join(BASE_DIR, '../../logs')

LOG_LEVEL = 'DEBUG'

DEBUG = True

SECRET_KEY = get_secret('secret_key')

ALLOWED_HOSTS = ['192.168.33.10', 'localhost']

DATABASES['default']['PASSWORD'] = get_secret('local_password')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_PATH, 'app.log')
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}

CORS_ORIGIN_ALLOW_ALL = True