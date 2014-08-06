from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models
from django.dispatch.dispatcher import receiver

from core.models import (GalleryAudio, Image, GalleryImage, SluggedModel, 
    TextContentModel
)

class Section(TextContentModel):
    page = models.ForeignKey('Page')
    heading = models.CharField(max_length=64)
    audio = generic.GenericRelation(GalleryAudio)
    #TODO map

    def __str__(self):
        return "({0}) {1}".format(self.page.full_name, self.heading)

class SectionGallery(models.Model):
    section = models.OneToOneField(Section)
    images = generic.GenericRelation(GalleryImage)
        
    def __str__(self):
        return str(self.section)
        
    def save(self, **kwargs):
        super().save(**kwargs)
        
        self.section.page.has_gallery = True
        self.section.page.save()

@receiver(models.signals.pre_delete, sender=SectionGallery)
def _sectiongallery_delete(sender, instance, **kwargs):
    section = instance.section
    section.page.update_bools(ignore_section_id=section.id)

class Page(SluggedModel):
    subheader_image = models.ForeignKey(Image, blank=True, null=True)
    has_gallery = models.BooleanField(default=False)
    has_map = models.BooleanField(default=False)
    
    def update_bools(self, ignore_section_id=None):
        has_gallery = False
        has_map = False
        
        for section in self.section_set.all():
            if section.id == ignore_section_id:
                continue
                
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
