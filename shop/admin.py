from django.contrib import admin
from . import models


class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time', 'update_time')
admin.site.register(models.Site, SiteAdmin)


class DomainAdmin(admin.ModelAdmin):
	list_display = ('domain','site', 'create_time', 'update_time')
admin.site.register(models.Domain, DomainAdmin)

class SiteConfigAdmin(admin.ModelAdmin):
	list_display = ('site','name','val','create_time', 'update_time')
admin.site.register(models.SiteConfig, SiteConfigAdmin)

