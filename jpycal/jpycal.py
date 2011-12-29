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


# URI parser


# dev server

def main(): run_wsgi_app(app)
if __name__ == '__main__': main()
