from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models

from core.models import AudioSet, Image, GalleryImage, SluggedModel

class Section(models.Model):
    page = models.ForeignKey('Page')
    heading = models.CharField(max_length=64)
    content = models.TextField()
    
    audio = generic.GenericRelation(AudioSet)
    images = generic.GenericRelation(GalleryImage)
    #map
    
    def __str__(self):
        return "({0}) {1}".format(self.page.full_name, self.heading)

class Page(SluggedModel):
    subheader_image = models.ForeignKey(Image, null=True)
    
