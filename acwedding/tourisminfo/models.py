from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
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
    external_links = generic.GenericRelation(GenericLink, verbose_name="External links")
    short_description = models.CharField(max_length=128)
    image = models.ForeignKey(Image, null=True, blank=True)
    
    def __str__(self):
        return self.full_name
        
    @property
    def full_name(self):
        return self.marker.location.full_name
        
    @property
    def location(self):
        return self.marker.location
        
    @property
    def slug(self):
        return self.marker.location.slug
    
    class Meta:
        abstract = True

class PointOfInterest(BasePointOfInterest):
    CATEGORY_CHOICES = (
        ('attractions', 'Things to Do'),
        ('food', 'Food & Drink'),
        ('lighthouses', 'Lighthouses'),
    )
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name_plural = 'Points of interest'
        ordering = ['marker__location__full_name']
    
class Accommodation(BasePointOfInterest):
    CATEGORY_CHOICES = (
        ('hotel', 'Hotels'),
        ('motel', 'Motels'),
        ('bandb', 'Bed and Breakfast'),
        ('cabin', 'Cabins / Cottages / Campgrounds / RV Parks'),
    )
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    category2 = models.CharField(max_length=16, choices=CATEGORY_CHOICES, 
        blank=True, null=True
    )
    amenities = CustomTextField(blank=True)
    
    def validate_unique(self, **kwargs):
        if self.category == self.category2:
            raise ValidationError('Categories must be unique')
            
        return super().validate_unique(**kwargs)
        
    class Meta:
        ordering = ['marker__location__full_name']
