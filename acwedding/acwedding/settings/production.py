from .base import *

STATIC_ROOT = BASE_DIR.parent.child('staticfiles')
ALLOWED_HOSTS = ['*']
DEBUG = True
TEMPLATE_DEBUG = False
