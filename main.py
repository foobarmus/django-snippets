"""
WSGI application for GAE.

For normal django deployment, django.wsgi is used instead.
""" 
import os, sys
sys.path.append('/Users/mark/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_snippets.settings'

from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp.util import run_wsgi_app
from django.conf import settings
settings._target = None
import django.core.handlers.wsgi

def main():
    application = django.core.handlers.wsgi.WSGIHandler()
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
