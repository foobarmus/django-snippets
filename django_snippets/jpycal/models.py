from google.appengine.ext import db

dfmt = '%Y-%m-%dT%H:%M:%S'

class Event(db.Model):
    """
    Define events to store in datastore.

    'end' is non-mandatory because the
    fullcalendar widget is able to render
    events without it, in certain situations.

    'url' is reserved for system use, to ease
    event retrieval. If you wish to attach
    a web link to the instance, create another
    attribute such as 'link'.

    Instantiation:
        myevent = Event(start=datetimeobject,
                        title='My Event')

    """
    start = db.DateTimeProperty(required=True)
    end = db.DateTimeProperty()
    allDay = db.BooleanProperty(default=False)
    title = db.StringProperty(required=True)
    description = db.StringProperty()
    url = db.StringProperty()

    def dict_(self):
        """
        Represent the instance in serializable form.

        Usage example:
            json.dumps(myevent.dict_())

        """
        jsonable = {
            'start': self.start.strftime(dfmt),
            'title': self.title,
            'url': self.url
        }
        if self.end:
            jsonable['end'] = self.end.strftime(dfmt)
        if self.description:
            jsonable['description'] = self.description
        if self.allDay:
            jsonable['allDay'] = True
        return jsonable

