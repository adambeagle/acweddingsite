from django.contrib.contenttypes import generic
from django.db import models

from core.models import CustomTextField, Image, GenericLink
from googlemaps.models import Marker

class BasePointOfInterest(models.Model):
    # To decouple this model from this project, use core.Location instead of 
    # googlemaps.Marker for similar functionality (Marker has a Location 
    # attribute).
    description = CustomTextField()
    marker = models.ForeignKey(Marker)
    review = CustomTextField(blank=True)
    highlight = models.BooleanField(default=False)
    external_links = generic.GenericRelation(GenericLink)
    short_description = models.CharField(max_length=128)
    image = models.ForeignKey(Image, null=True, blank=True)
        
    @property
    def location(self):
        return self.marker.location
    
    class Meta:
        abstract = True
        
class PointOfInterest(BasePointOfInterest):
    CATEGORY_CHOICES = (
        ('attractions', 'Things to Do'),
        ('food', 'Food & Drink'),
        ('lighthouses', 'Lighthouses'),
    )
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    
class Accommodation(BasePointOfInterest):
    CATEGORY_CHOICES = (
        ('hotel', 'Hotel'),
        ('motel', 'Motel'),
        ('cabins', 'Cabins'),
        ('bandb', 'Bed and Breakfast'),
    )
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    