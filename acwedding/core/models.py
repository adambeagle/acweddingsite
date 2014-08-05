import re

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

import core.util
    
# ============================================================================
# BASE CLASSES
class BaseAudio(models.Model):
    filename = models.FilePathField(
        path=settings.BASE_DIR.child('static', 'audio'),
        recursive=True,
        max_length=64
    )
    caption = models.CharField(max_length=128)
    
    def __str__(self):
        return self.filename
    
    def save(self, *args, **kwargs):
        self.filename = re.match(
            r".*/static/(audio/.*)$", self.filename
        ).group(1)
        
        return super().save(*args, **kwargs)
        
    class Meta:
        abstract = True

class BaseImage(models.Model):
    filename = models.FilePathField(
        path=settings.BASE_DIR.child('static', 'images'),
        recursive=True,
        max_length=128,
    )
    alt_text = models.CharField(max_length=64, null=True, blank=True)
    caption  = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.filename
        
    def save(self, *args, **kwargs):
        self.filename = re.match(
            r".*/static/(images/.*)$", self.filename
        ).group(1)
        
        return super().save(*args, **kwargs)
    
    class Meta:
        abstract = True

# TODO Auto-create slug with slugify on save()?
# Alternative is prepopulate in admin 
class SluggedModel(models.Model):
    full_name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        abstract = True
        
class TextContentModel(models.Model):
    content = models.TextField()
    
    def save(self, *args, **kwargs):
        """
        Perform custom processing on content before save (reverse urls, etc)
        """
        self.content = util.reverse_urls(
            util.rst_to_table(util.asterisks_to_ul(self.content))
        )
        
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True
#=============================================================================
class Audio(BaseAudio):
    pass
    
class AudioSet(BaseAudio):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() # Change?
    content_object = generic.GenericForeignKey('content_type', 'object_id')
        
class GalleryImage(BaseImage):
    """Use with GenericRelation to give external model multiple images."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() # Change?
    content_object = generic.GenericForeignKey('content_type', 'object_id')
        
class Image(BaseImage):
    """Use with ForeignKey to give external model single image."""
    pass
        
class Link(models.Model):
    url = models.URLField()
    text = models.CharField(max_length=64)
    title = models.CharField(max_length=32)
    
    def __str__(self):
        return "{0} ({1})".format(self.text, self.url)
    
class Location(SluggedModel):
    latitude = models.FloatField()
    longitude = models.FloatField()


