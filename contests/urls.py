try:
    from django.conf.urls import url, patterns
except ImportError:
    # for Django version less than 1.4
    from django.conf.urls.defaults import url, patterns

from .views import ContestDetailView, EntryCreateView, WinnerDetailView, EntryReceivedView

urlpatterns = patterns('',
    url('^contests/(?P<slug>[a-zA-Z0-9-]+)/$', ContestDetailView.as_view(), name='contest-detail'),
    url('^contests/(?P<slug>[a-zA-Z0-9-]+)/enter/$', EntryCreateView.as_view(), name='contest-entry'),
    url('^contests/(?P<slug>[a-zA-Z0-9-]+)/enter/received/$', EntryReceivedView.as_view(), name='contest-entry-received'),
    url('^contests/(?P<slug>[a-zA-Z0-9-]+)/winner/(?P<uuid>[a-zA-Z0-9\-]+)/$', WinnerDetailView.as_view(), name='contest-winner'),

)
