from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from .util import linkable_latitude, linkable_longitude
from core.models import BaseStaticFile, Location

class Icon(BaseStaticFile):
    full_path = models.FilePathField(
        path=settings.BASE_DIR.child('static', 'images', 'map_icons'),
        max_length=128,
    )
    
    def __str__(self):
        return self.filename

class Marker(models.Model):
    """Defines a marker for use in an embedded Google Map"""
    
    # 'name' used for JS variable naming when creating map
    # (hence must be unique, should be camel case)
    name = models.CharField(max_length=16, unique=True)
    location = models.ForeignKey(Location)
    icon = models.ForeignKey(Icon)
    
    def __str__(self):
        return self.location.full_name
    
class BaseMap(models.Model):
    name = models.CharField(max_length=16, primary_key=True)
    start_lat = models.FloatField(verbose_name='Starting Latitude')
    start_long = models.FloatField(verbose_name='Starting Longitude')
    start_zoom = models.PositiveSmallIntegerField(
        verbose_name='Starting Zoom',
        default=15
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        
class MultiMarkerMap(BaseMap):
    full_map_url = models.URLField(max_length=256, blank=True)
    markers = models.ManyToManyField(Marker)
    
    #~ def save(self, **kwargs):
        #~ if not self.full_map_url:
            #~ s = "http://google.com/maps/place/{0}+{1}/@{2},{3},{4}z".format(
                #~ linkable_latitude(self.start_lat),
                #~ linkable_longitude(self.start_long),
                #~ self.start_lat, 
                #~ self.start_long,
                #~ self.start_zoom
            #~ )
            #~ self.full_map_url = s

        #~ super().save(**kwargs)
    
    @cached_property
    def static_map_url(self):
        return "" # TODO