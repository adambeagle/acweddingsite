from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faq/', include('faq.urls', namespace='faq')),
    #url(r'^area-information/', include('tourisminfo.urls', namespace='tourisminfo')),
    url(r'^', include('pages.urls', namespace='pages')),
)

