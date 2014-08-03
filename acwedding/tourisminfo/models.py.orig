from os.path import basename

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from googlemaps.models import Marker

class PointOfInterest(models.Model):
    CATEGORY_CHOICES = (
        ('attractions', 'Attractions'),
        ('food', 'Food'),
        ('lighthouses', 'Lighthouses'),
    )
    marker = models.OneToOneField(Marker, primary_key=True)
    slug = models.SlugField(
        max_length=100) # Should match marker.full_name's max_length
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    short_description = models.CharField(max_length=128)
    description = models.TextField()
    review = models.TextField(blank=True)
    link = models.URLField(blank=True)
    link_description = models.CharField(max_length=20, default='Website', blank=True)
    highlight = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name
        
    def save(self, *args, **kwargs):
        """Automatically generate slug from full_name"""
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.marker.full_name
        
    @property
    def name(self):
        return self.marker.name
        
    class Meta:
        ordering = ['marker']
        verbose_name_plural = 'Points of interest'
        
class Image(models.Model):
    point_of_interest = models.OneToOneField(PointOfInterest)
    full_path = models.FilePathField(path=settings.BASE_DIR.child(
        'static', 'images', 'tourisminfo'), 
        blank=True,
        max_length=200)
    alt_text = models.CharField(max_length=50, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.filename
    
    @property
    def filename(self):
        return basename(self.full_path)