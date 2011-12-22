from os import path

DEBUG = True # REMEMBER TO CHANGE FOR PRODUCTION!!
TEMPLATE_DEBUG = DEBUG
DIR = path.abspath(path.dirname(__file__))
DATABASE_ENGINE = '' # DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '' # DATABASE_NAME = DIR + '/db/spaghetti_mess.db'
TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-AU'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = DIR + '/static/'
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
SECRET_KEY = '<YOUR_SECRET_KEY>'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)
ROOT_URLCONF = 'django_snippets.urls'
TEMPLATE_DIRS = (
    DIR + 'templates',
    DIR + 'search_the_web/templates',
    DIR + 'jpycal/templates',
)
INSTALLED_APPS = (
    'django_snippets.search_the_web',
    'django_snippets.jpycal',
)
