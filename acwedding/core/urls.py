from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import PageDetailView

urlpatterns = patterns('',
    # Redirect root to /welcome
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('core:detail', args=['welcome']))),
        
    url(r'^(?P<pk>\w+)/$', PageDetailView.as_view(), name="detail"),
)
