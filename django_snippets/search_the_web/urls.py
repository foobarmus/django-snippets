from django.conf.urls.defaults import patterns

urlpatterns = patterns('django_snippets.search_the_web.views',
    (r'^', 'search'),
)
