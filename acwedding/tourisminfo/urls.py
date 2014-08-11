from django.conf.urls import patterns, url

from .views import (AccommodationDetailView, AccommodationIndexView, 
    PointOfInterestIndexView, PointOfInterestDetailView
)

urlpatterns = patterns('',
    url(r'^accommodations/$',
        AccommodationIndexView.as_view(),
        name='accommodations_index'
    ),
    url(r'^accommodations/(?P<slug>[\w-]+)/$', 
        AccommodationDetailView.as_view(), 
        name="accommodation_detail"
    ),
    url(r'^attractions-and-food/$', 
        PointOfInterestIndexView.as_view(), 
        name="attractions_index"
    ),
    url(r'^attractions-and-food/(?P<slug>[\w-]+)/$', 
        PointOfInterestDetailView.as_view(), 
        name="attraction_detail"
    ),
)
