from django.contrib import admin

from .models import Icon, Marker, SimpleMap

admin.site.register(Icon)
admin.site.register(Marker)
admin.site.register(SimpleMap)