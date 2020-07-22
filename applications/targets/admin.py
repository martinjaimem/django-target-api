from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from applications.targets.models import Target, Topic


class TargetAdmin(OSMGeoAdmin):
    fields = ('title', 'owner', 'topic', 'location', 'radius')
    list_display = ('title', 'owner', 'topic', 'location', 'radius')
    search_fields = ['title', 'topic']


admin.site.register(Target, TargetAdmin)
admin.site.register(Topic)
