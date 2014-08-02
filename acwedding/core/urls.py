from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import ContactView, PageDetailView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='core/welcome.html'), name='welcome'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^contact/thanks/$', TemplateView.as_view(template_name='core/contact_thanks.html'), name='contact_thanks'),
    url(r'^(?P<slug>[\w-]+)/$', PageDetailView.as_view(), name='detail'),
)
