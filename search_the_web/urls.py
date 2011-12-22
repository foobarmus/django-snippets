from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    (r'^', 'django_snippets.search_the_web.views.search'),
)
