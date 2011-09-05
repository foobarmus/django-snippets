import os, sys
sys.path.append('/home/mark/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
