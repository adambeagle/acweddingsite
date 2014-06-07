from os.path import basename

from django.db import models
from django.conf import settings

from googlemaps.models import SimpleMap


class Page(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.title
        
class SubheaderImage(models.Model):
    page = models.OneToOneField(Page)
    full_path = models.FilePathField(path=settings.BASE_DIR.child(
        'static', 'images', 'subheaders'), 
        blank=True,
        max_length=200)
    alt_text = models.CharField(max_length=50, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.filename
    
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
        
    class Meta:
        verbose_name_plural = 'Mini Galleries'
        
class SectionAudio(models.Model):
    section = models.ForeignKey(Section)
    full_path = models.FilePathField(path=settings.BASE_DIR.child(
        'static', 'audio'),
        max_length=256)
    filename = models.CharField(max_length=64)
    description = models.TextField()
    
    def __str__(self):
        return self.filename
        
    def save(self, *args, **kwargs):
        """
        Automatically generate filename from full_name.
        """
        self.filename = basename(self.full_path)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Section audio'
        ordering = ('filename', )
        