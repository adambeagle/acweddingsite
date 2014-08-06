from django.contrib import admin
from django.contrib.contenttypes import generic

from .models import GalleryAudio, Image, GalleryImage, Location

class GalleryImageInline(generic.GenericTabularInline):
    model = GalleryImage
    extra = 0
    
class GalleryAudioInline(generic.GenericTabularInline):
    model = GalleryAudio
    extra = 0
    
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('full_name', )}

admin.site.register(Image)
admin.site.register(Location, LocationAdmin)
