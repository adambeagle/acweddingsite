from os.path import basename

from django.db import models
from django.conf import settings

from googlemaps.models import SimpleMap

class Page(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubheaderImage(models.Model):
    page = models.OneToOneField(Page)
    full_path = models.FilePathField(path=settings.BASE_DIR.child(
        'static', 'images', 'subheaders'), 
        blank=True,
        max_length=200)
    alt_text = models.CharField(max_length=50, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    
    @property
    def filename(self):
        return basename(self.full_path)
        
class Section(models.Model):
    page = models.ForeignKey(Page)
    heading = models.CharField(max_length=50)
    content = models.TextField()
    map = models.ForeignKey(SimpleMap, null=True, blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return "({0}) {1}".format(self.page, self.heading)

class MiniGalleryImage(models.Model):
    full_path = models.FilePathField(path=settings.BASE_DIR.child(
        'static', 'images', 'minigallery'),
        max_length=200)
    caption = models.CharField(max_length=100)
        
    def __str__(self):
        return self.filename
        
    @property
    def filename(self):
        return basename(self.full_path)
        
class MiniGallery(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    section = models.OneToOneField(Section)
    images = models.ManyToManyField(MiniGalleryImage)
    
    def __str__(self):
        return self.name