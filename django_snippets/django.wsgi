"""
WSGI application for normal django deployment.

For GAE deployment, gae.py is used instead.
""" 
import os, sys
sys.path.append('/project/parent/dir/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_snippets.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
