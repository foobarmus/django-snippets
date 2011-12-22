from django.shortcuts import render_to_response
from django.template import Context

from django_snippets.jpycal.models import User

# main page

class calendar(webapp.RequestHandler):

    def get(self):
        self.response.out.write(template.render(c_page, {}))

# API

class event(webapp.RequestHandler):

    def get(self, args):
        """
        Deliver requested event as json or html.

        This method is not used at the moment, but
        in a real-life situation it might come in
        handy.

        For example, you could request json from
        the eventMouseOver in fullcalendar, and
        display the description in a bubble.

        Or request html from another app, eg...
        http://jpycal.skagos.com.au/event/3001

        """
        id_ = int(args.split('/')[1])

        # fetch the event
        e = Event.get_by_id(id_)

        # format and deliver based on expected output
        accept = self.request.headers['Accept']
        if accept and accept == 'application/json':
            self.response.headers.add_header('content-type', 'application/json')
            self.response.out.write(json.dumps(e.dict_()))
        else:
            self.response.out.write(template.render(e_page, {'e':e}))

    def post(self, args):
        """create an event"""
        f = rip(cgi.FieldStorage())

        # create and store the event
        e = Event(**f)
        e.put()

        # now we have an id, create the url
        e.url = event_url % e.key().id()
        e.put()

        # respond for good measure
        self.response.out.write('Event added')

    def put(self, args):
        """update an event"""
        id_ = int(args.split('/')[1])
        f = rip(cgi.FieldStorage())

        # fetch the event
        e = Event.get_by_id(id_)

        # update and save
        e.start = f['start']
        e.end = f.has_key('end') and f['end'] or e.end
        e.allDay = f.has_key('allDay') and f['allDay'] or e.allDay
        e.title = f.has_key('title') and f['title'] or e.title
        e.description = f.has_key('description') and f['description'] or e.description
        e.put()

        # respond
        self.response.out.write('Event updated')

class batch(webapp.RequestHandler):
    """
    Find events within a given date range.

    This web service is used by fullcalendar
    to initialise calendar views, such as
    during the initial page load, or when you
    press 'month|week|day'.

    """
    def get(self):
        """output a batch of events as json"""
        f = rip(cgi.FieldStorage())

        # fetch the events
        events = Event.gql(q, **f)

        # format and deliver
        self.response.headers.add_header('content-type', 'application/json')
        self.response.out.write(json.dumps([e.dict_() for e in events]))

