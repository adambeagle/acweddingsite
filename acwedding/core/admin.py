from django.contrib import admin

from .models import (MiniGallery, MiniGalleryImage, Page, Section, 
    SubheaderImage)
    
# Inlines
#~ class MiniGalleryImageInline(admin.TabularInline):
    #~ model = MiniGalleryImage
    #~ extra = 1

class SectionInline(admin.StackedInline):
    model = Section
    #fields = ('heading', 'content', 'map')
    extra = 0

class SubheaderImageInline(admin.TabularInline):
    model = SubheaderImage

# ModelAdmins
#~ class MiniGalleryAdmin(admin.ModelAdmin):
    #~ inlines = [MiniGalleryImageInline]
    
class PageAdmin(admin.ModelAdmin):
    inlines = [SubheaderImageInline, SectionInline]

# Registration
admin.site.register(MiniGallery)
admin.site.register(MiniGalleryImage)
admin.site.register(Page, PageAdmin)