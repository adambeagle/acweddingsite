from os.path import basename, splitext

from django.db import models
from django.conf import settings

class Icon(models.Model):
    path = models.FilePathField(path=settings.BASE_DIR.child(
        'static', 'images', 'map_icons'))
    
    def __str__(self):
        return self.name
        
    @property
    def filename(self):
        return basename(self.path)
        
    @property
    def name(self):
        """ """
        return splitext(self.filename)[0]
        
class Marker(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    full_name = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    icon = models.ForeignKey(Icon)
    
    def __str__(self):
        return self.full_name

class Map(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    startLat = models.FloatField()
    startLong = models.FloatField()
    startZoom = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

class SimpleMap(Map):
    full_map_link = models.URLField(blank=True)
    markers = models.ManyToManyField(Marker, blank=True)
