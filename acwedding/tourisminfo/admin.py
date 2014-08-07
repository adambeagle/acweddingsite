from django.contrib import admin

from .models import Accommodation, PointOfInterest
from core.admin import GenericLinkInline

class PointOfInterestAdmin(admin.ModelAdmin):
    fields = ('marker', 'category', 'short_description', 'content',  
        'review', 'image', 'highlight'
    )
    inlines = (GenericLinkInline, )

admin.site.register(Accommodation, PointOfInterestAdmin)
admin.site.register(PointOfInterest, PointOfInterestAdmin)
