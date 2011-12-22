"""
WSGI application for normal django deployment.

For GAE deployment, main.py is used instead.
""" 
import os, sys
sys.path.append('/Users/mark/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_snippets.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
