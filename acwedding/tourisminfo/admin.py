from django.contrib import admin

from .models import Image, PointOfInterest

class ImageInline(admin.TabularInline):
    model = Image
    
class PointOfInterestAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    
admin.site.register(PointOfInterest, PointOfInterestAdmin)
