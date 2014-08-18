from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models
from django.dispatch.dispatcher import receiver

from core.models import (CustomTextField, GalleryAudio, Image, 
    GalleryImage, SluggedModel
)
from googlemaps.models import MultiMarkerMap

class Section(models.Model):
    content = CustomTextField()
    page = models.ForeignKey('Page')
    heading = models.CharField(max_length=64)
    audio = generic.GenericRelation(GalleryAudio)
    map = models.ForeignKey(
        MultiMarkerMap, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "({0}) {1}".format(self.page.full_name, self.heading)
        
    def save(self, **kwargs):
        super().save(**kwargs)
        if self.map is not None:
            self.page.has_map = True
            self.page.save()
            
    class Meta:
        ordering = ['id']

class SectionGallery(models.Model):
    section = models.OneToOneField(Section)
    images = generic.GenericRelation(GalleryImage)
        
    def __str__(self):
        return str(self.section)
        
    def save(self, **kwargs):
        super().save(**kwargs)
        
        self.section.page.has_gallery = True
        self.section.page.save()
        
    class Meta:
        verbose_name_plural = 'Section galleries'

@receiver(models.signals.pre_delete, sender=(SectionGallery, MultiMarkerMap))
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
                
            if section.map is not None:
                has_map = True
            
            if has_gallery and has_map:
                break
            
        self.has_gallery = has_gallery
        self.has_map = has_map
        self.save()
        
    @property
    def title(self):
        return self.full_name
