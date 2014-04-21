from django.contrib import admin

from .models import (MiniGallery, MiniGalleryImage, Page, Section, 
    SubheaderImage)
    
class SectionInline(admin.StackedInline):
    model = Section
    extra = 0

class SubheaderImageInline(admin.TabularInline):
    model = SubheaderImage

class PageAdmin(admin.ModelAdmin):
    inlines = [SubheaderImageInline, SectionInline]

admin.site.register(MiniGallery)
admin.site.register(MiniGalleryImage)
admin.site.register(Page, PageAdmin)