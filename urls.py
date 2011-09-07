from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('snippets.search_the_web.urls')),
)
