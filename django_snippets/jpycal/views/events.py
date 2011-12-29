"""
Controllers for jpycal.
Author: Mark Donald <mark@skagos.com.au>

The dispatch function sends requests to
dispatcher.py which invokes the appropriate
controller. For example:

/events (GET)  > get(request)
/events (POST) > post(request)

and so on...

"""
from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson as json

from django_snippets.jpycal.models import Event
from dispatcher import resource

# constants

iso = '%Y-%m-%d %H:%M'
json_hdr = 'application/json'
event_url = '/event/%s'
q = "WHERE start >= :start AND start < :end"
boundary_dates = ('start', 'end')

# form ripper

def rip(params):
    data = {}
    for k in params:
        k = str(k)
        if k == 'allDay':
            data[k] = (params[k] == 'true') and True or False
        elif k in boundary_dates:
            if '-' in params[k]:
                # convert from ISO
                data[k] = datetime.strptime(params[k], iso)
            else:
                # convert from POSIX
                data[k] = datetime.fromtimestamp(float(params[k]))
        else:
            data[k] = params[k]
    return data

# collection handlers

def get(request):
    """
    Finds events within a given date range;
    spits out a batch of events as json.

    This web service is used by fullcalendar
    to initialise calendar views, such as
    during the initial page load, or when you
    press 'month|week|day'.

    """
    f = rip(request.GET)

    # fetch the events
    events = Event.gql(q, **f)

    # format and deliver
    return HttpResponse(json.dumps([e.dict_() for e in events]),
                        mimetype=json_hdr)

def post(request):
    """create an event"""
    f = rip(request.POST)

    # create and store the event
    e = Event(**f)
    e.put()

    # now we have an id, create the url
    e.url = event_url % e.key().id()
    e.put()

    # respond for good measure
    return HttpResponse('Event added')

# item handlers

class event:

    def __init__(self, request, id_, data):
        self.request = request
        self.id = id_
        self.f = rip(data)

    def get(self):
        """
        Deliver an event as json or html.

        This method is included for the sake of
        completeness. Though unused, it might
        come in handy in a real-life situation.

        For example, you could request json from
        the eventMouseOver in fullcalendar, and
        display the description in a bubble, or
        request html from another app. For
        example,

        http://mydomain.com/jpycal/event/3001

        """
        # fetch the event
        e = Event.get_by_id(self.id)

        # format and deliver, based on expected output
        accept = self.request.META['HTTP_ACCEPT']
        if accept and accept == json_hdr:
            return HttpResponse(json.dumps(e.dict_()),
                                mimetype=json_hdr)
        else:
            return render_to_response('event.html', {'e':e})

    def put(self):
        """update an event"""
        f = self.f

        # fetch the event
        e = Event.get_by_id(self.id)

        # update and save
        e.start = f.has_key('start') and f['start'] or e.start
        e.end = f.has_key('end') and f['end'] or e.end
        if f.has_key('allDay'):
            e.allDay = f['allDay']
        e.title = f.has_key('title') and f['title'] or e.title
        e.description = f.has_key('description') and \
                            f['description'] or e.description
        e.put()

        # respond
        return HttpResponse('Event updated')

r = resource(get, post, event)
def dispatch(request, id=None):
    return r.dispatch(request, id)
