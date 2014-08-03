from django.contrib import admin
from django.contrib.contenttypes import generic

from .models import Image, GalleryImage

class GalleryImageInline(generic.GenericTabularInline):
    model = GalleryImage
    extra = 0

admin.site.register(Image)

#~ from .models import (MiniGallery, MiniGalleryImage, Page, Section, 
    #~ SectionAudio, SubheaderImage)
    
#~ class SectionInline(admin.StackedInline):
    #~ model = Section
    #~ extra = 0

#~ class SubheaderImageInline(admin.TabularInline):
    #~ model = SubheaderImage

#~ class PageAdmin(admin.ModelAdmin):
    #~ prepopulated_fields = {'slug' : ('title', )}
    #~ inlines = [SubheaderImageInline, SectionInline]
    
#~ class SectionAudioAdmin(admin.ModelAdmin):
    #~ exclude = ('filename', )

#~ admin.site.register(SectionAudio, SectionAudioAdmin)
#~ admin.site.register(MiniGallery)
#~ admin.site.register(MiniGalleryImage)
#~ admin.site.register(Page, PageAdmin)