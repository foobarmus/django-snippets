'''
Db model and request handlers for jpycal.
Author: Mark Donald <mark@skagos.com.au>
'''
from os import path
from datetime import datetime
import cgi, sys

from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson as json

# environment and constants

tpath = path.join(path.join(path.dirname(__file__), 'templates'), '')
c_page = tpath + 'calendar.html'
e_page = tpath + 'event.html'
dfmt = '%Y-%m-%dT%H:%M:%S'
event_url = '/event/%s'
q = "WHERE start >= :start AND start < :end"
boundary_dates = ('start', 'end')

# form ripper

def rip(fs):
    data = {}
    for k in fs:
        if k == 'allDay':
            data[k] = (fs[k].value == 'true') and True or False
        elif k in boundary_dates:
            if '-' in fs[k].value:
                # convert from ISO
                data[k] = datetime.strptime(fs[k].value, '%Y-%m-%d %H:%M')
            else:
                # convert from POSIX
                data[k] = datetime.fromtimestamp(float(fs[k].value))
    return data

# URI parser

app = webapp.WSGIApplication([('/event(.*)', event),
                               ('/batch', batch),
                               ('/.*', calendar)],
                              debug=True)

# dev server

def main(): run_wsgi_app(app)
if __name__ == '__main__': main()
