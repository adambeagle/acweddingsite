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
    fields = ('heading', 'content', 'map')
    inlines = [GalleryAudioInline]
    
    def has_add_permission(self, request):
        return False
    
class SectionGalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionGallery, SectionGalleryAdmin)
