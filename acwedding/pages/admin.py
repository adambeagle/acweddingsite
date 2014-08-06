from django.contrib import admin

from core.admin import GalleryAudioInline, GalleryImageInline
from .models import Page, Section, SectionGallery

class SectionInline(admin.StackedInline):
    model = Section
    fields = ('heading', 'content')
    extra = 0
    
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('full_name', )}
    fields = ('full_name', 'slug', 'subheader_image')
    inlines = [SectionInline]
    
class SectionAdmin(admin.ModelAdmin):
    inlines = [GalleryAudioInline]
    
class SectionGalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionGallery, SectionGalleryAdmin)
