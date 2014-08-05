from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models

from core.models import (AudioSet, Image, GalleryImage, SluggedModel, 
    TextContentModel
)

class Section(TextContentModel):
    page = models.ForeignKey('Page')
    heading = models.CharField(max_length=64)
    
    audio = generic.GenericRelation(AudioSet)
    gallery_images = generic.GenericRelation(GalleryImage)
    #TODO map
    
    def __str__(self):
        return "({0}) {1}".format(self.page.full_name, self.heading)
        
    def delete(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        Page.objects.get(pk=self.page.id).update_bools()
        
        return ret
        
    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        self.page.update_bools()
        
        return ret

class Page(SluggedModel):
    subheader_image = models.ForeignKey(Image, null=True)
    has_gallery = models.BooleanField(default=False)
    has_map = models.BooleanField(default=False)
    
    def update_bools(self):
        has_gallery = False
        has_map = False
        
        for section in self.section_set.all():
            if section.gallery_images.all():
                has_gallery = True
                
            # TODO check map
            
            if has_gallery and has_map:
                break
            
        self.has_gallery = has_gallery
        self.has_map = has_map
        self.save()
        
    @property
    def title(self):
        return self.full_name
                
                
