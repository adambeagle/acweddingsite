from django.contrib import admin
from django.contrib.contenttypes import generic

from .models import Image, GalleryAudio, GalleryImage, GenericLink, Location

class GalleryImageInline(generic.GenericTabularInline):
    model = GalleryImage
    extra = 0
    
class GalleryAudioInline(generic.GenericTabularInline):
    model = GalleryAudio
    extra = 0
    
class GenericLinkInline(generic.GenericTabularInline):
    model = GenericLink
    extra = 1
    
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('full_name', )}

admin.site.register(Image)
admin.site.register(Location, LocationAdmin)
