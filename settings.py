# Django settings for snippets project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/usr/local/django/snippets/db/spaghetti_mess.db'
TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-AU'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = '/usr/local/django/snippets/static/'
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
SECRET_KEY = '<YOUR_SECRET_KEY>'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'snippets.urls'
TEMPLATE_DIRS = (
    '/usr/local/django/snippets/templates',
    '/usr/local/django/snippets/search_the_web/templates',
)
INSTALLED_APPS = (
    'snippets.search_the_web',
)
