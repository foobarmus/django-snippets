from django.http import Http404

class UnknownMethod(ValueError):
    pass

class resource:

    def __init__(self, get, post, member_class):
        self.get=get
        self.post=post
        self.member_class = member_class

    def dispatch(self, request, id=None):
        try:
            # items
            if id:
                id = int(id)
                if request.method == 'GET':
                    item = self.member_class(request, id, request.GET)
                    return item.get()
                elif request.method == 'PUT':
                    r = self._coerce(request, 'PUT')
                    item = self.member_class(r, id, r.PUT)
                    return item.put()

                # overloaded POST requests
                elif request.method == 'POST' and \
                 request.POST.has_key('method') and \
                 request.POST['method'].lower() == 'put':
                    item = self.member_class(request, id, request.POST)
                    return item.put()
                else:
                    raise UnknownMethod

            # collections
            else:
                if request.method == 'GET':
                    return self.get(request)
                elif request.method == 'POST':
                    return self.post(request)
                else:
                    raise UnknownMethod

        except UnknownMethod:
            raise Http404

    def _coerce(self, request, verb):
        """
        Treat PUT/DELETE request data as form-urlencoded.

        Django doesn't do this by itself because PUT/DELETE
        requests are not usually made by browsers and therefore
        the payload probably isn't in that format.

        We are handling PUT requests only because this is an
        example app, and the RESTful API should be able to
        accept direct PUT requests from other apps (in which
        case the payload should be type-checked and parsed
        appropriately - which we are not doing, for the sake of
        brevity).

        Fullcalendar is configured to issue PUTs as overloaded
        POST requests, in accordance with the HTML5 spec.

        """
        if request.method == verb:
            if hasattr(request, '_post'):
                del(request._post)
                del(request._files)

            request.method = "POST"
            request._load_post_and_files()
            request.method = verb
            setattr(request, verb, request.POST)

        return request
