from os import environ

from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'acwedding',
        'USER' : environ['DB_USERNAME'],
        'PASSWORD' : environ['DB_PASSWORD'],
        'HOST' : '',
        'PORT' : '',
    }
}

STATIC_ROOT = BASE_DIR.child('static', 'static_root')
