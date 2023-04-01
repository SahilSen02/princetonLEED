from django.contrib import admin
from dashboard.models import Building
# Register your models here.


class BuildingAdmin(admin.ModelAdmin):
    list_display = ['property_name']
    ordering = ['property_name']
    # actions = [make_published]


admin.site.register(Building, BuildingAdmin)
