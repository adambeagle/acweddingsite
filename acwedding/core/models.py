from os.path import basename
import re

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.functional import cached_property

from core import util

#================================================================
# CUSTOM FIELDS
class CustomTextField(models.TextField):
    def to_python(self, value):
        value = util.reverse_urls(
            util.rst_to_table(value)
        )
        return super().to_python(value)
    
# ============================================================================
# BASE CLASSES
class BaseStaticFile(models.Model):
    """
    Designed for use with models that represent or point to a static asset.
    Provides static_path and filename cached properties.
    """
    def __str__(self):
        return self.static_path
    
    @cached_property
    def filename(self):
        return basename(self.full_path)
    
    @cached_property
    def static_path(self):
        return re.match(
            r".*/static/(.+)$", self.full_path
        ).group(1)
        
    class Meta:
        abstract = True

class BaseAudio(BaseStaticFile):
    full_path = models.FilePathField(
        path=settings.BASE_DIR.child('static', 'audio'),
        recursive=True,
        max_length=128
    )
    caption = models.CharField(max_length=128)
    
    class Meta:
        abstract = True

class BaseImage(BaseStaticFile):
    
    full_path = models.FilePathField(
        path=settings.BASE_DIR.child('static', 'images'),
        recursive=True,
        max_length=128,
    )
    alt_text = models.CharField(max_length=64, null=True, blank=True)
    caption  = models.CharField(max_length=256, null=True, blank=True)
        
    @cached_property
    def thumbnail_path(self):
        return re.sub(
            r"^images/(?:.*/)*(.+)$", 
            r'images/tn/\1',
            self.static_path
        )

    class Meta:
        abstract = True
        
class BaseLink(models.Model):
    url = models.URLField()
    text = models.CharField(max_length=64)
    title = models.CharField(max_length=32)
    
    def __str__(self):
        return "{0} ({1})".format(self.text, self.url)
        
    class Meta:
        abstract = True
        ordering = ['text']

class SluggedModel(models.Model):
    full_name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        abstract = True

#=============================================================================
class Audio(BaseAudio):
    pass
    
class GalleryAudio(BaseAudio):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() # Change?
    content_object = generic.GenericForeignKey('content_type', 'object_id')
        
class GalleryImage(BaseImage):
    """Use with GenericRelation to give external model multiple images."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() # Change?
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['id']
        
class Image(BaseImage):
    """Use with ForeignKey to give external model single image."""
    pass
        
class GenericLink(BaseLink):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() 
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
class Link(BaseLink):
    pass
    
class Location(SluggedModel):
    latitude = models.FloatField()
    longitude = models.FloatField()


