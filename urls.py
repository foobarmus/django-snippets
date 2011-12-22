from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('django_snippets.search_the_web.urls')),
)
