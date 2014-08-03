from django.contrib import admin

from core.admin import GalleryImageInline
from .models import Page, Section

class SectionInline(admin.StackedInline):
    model = Section
    extra = 0
    
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('full_name', )}
    inlines = [SectionInline]
    
class SectionAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
