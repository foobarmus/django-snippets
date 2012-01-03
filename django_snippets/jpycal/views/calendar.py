"""
Calendar page renderer for jpycal.
Author: Mark Donald <mark@skagos.com.au>

All else is done with AJAX.

"""
from django.shortcuts import render_to_response

def get(request):
    return render_to_response('calendar.html', {})
