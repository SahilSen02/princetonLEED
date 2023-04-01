from django.contrib import admin
from dashboard.models import LL84Building
from dashboard.models import BINLookup
# Register your models here.


class LL84BuildingAdmin(admin.ModelAdmin):
    list_display = ['property_name']
    ordering = ['property_name']
    # actions = [make_published]


class BINLookupAdmin(admin.ModelAdmin):
    list_display = ['nyc_bin', 'building']
    ordering = ['building']
    # actions = [make_published]


admin.site.register(LL84Building, LL84BuildingAdmin)
admin.site.register(BINLookup, BINLookupAdmin)
