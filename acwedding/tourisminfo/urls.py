from django.conf.urls import patterns, url

from .views import AttractionsIndexView, POIDetailView

urlpatterns = patterns('',
    url(r'^attractions-and-food/$', AttractionsIndexView.as_view(), name="attractions_index"),
    url(r'^attractions-and-food/(?P<pk>\w+)/$', POIDetailView.as_view(), name="detail"),
)
