from django.conf.urls.defaults import patterns

urlpatterns = patterns('django_snippets.jpycal.views',
   ('^/events', 'events.dispatch'),
   (r'^/event/(?P<id>\d+)', 'events.dispatch'),
   ('^', 'calendar.get'),
)
