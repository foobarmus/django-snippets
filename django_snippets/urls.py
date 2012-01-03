from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^jpycal', include('django_snippets.jpycal.urls')),
    (r'^search', include('django_snippets.search_the_web.urls')),
)
